"""Portable, integrity-checked LoRA checkpoints; no cloud SDK or pickle loading.

Integrity hashes detect incomplete/corrupted copies. They do not authenticate an
untrusted producer. Only resume checkpoints created by a trusted training run.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
from datetime import datetime, timezone
import uuid
import zipfile

MANIFEST_NAME = "checkpoint_manifest.json"
LATEST_NAME = "latest.json"
CHECKPOINT_NAME = re.compile(r"checkpoint-[0-9]+\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
REQUIRED_METADATA = (
    "model_id", "model_revision", "split_manifest_sha256",
    "training_dataset_sha256", "chat_template_sha256",
)
REQUIRED_FILES = (
    "adapter_config.json", "optimizer.pt", "scheduler.pt",
    "trainer_state.json", "rng_state.pth",
)


class CheckpointError(ValueError):
    """A checkpoint is incomplete, incompatible, or unsafe to copy."""


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _metadata(metadata: dict) -> dict:
    if not isinstance(metadata, dict):
        raise CheckpointError("Checkpoint metadata must be an object")
    for key in REQUIRED_METADATA:
        if not isinstance(metadata.get(key), str) or not metadata[key]:
            raise CheckpointError(f"Missing checkpoint metadata: {key}")
    if not re.fullmatch(r"[0-9a-f]{40}", metadata["model_revision"]):
        raise CheckpointError("model_revision must be a pinned 40-character commit")
    for key in REQUIRED_METADATA:
        if key.endswith("_sha256") and not SHA256.fullmatch(metadata[key]):
            raise CheckpointError(f"Invalid SHA256 metadata: {key}")
    return metadata


def _checkpoint_dir(path: str | Path) -> Path:
    path = Path(path)
    if path.is_symlink() or not path.is_dir():
        raise CheckpointError("Checkpoint must be an existing, non-symlink directory")
    if not CHECKPOINT_NAME.fullmatch(path.name):
        raise CheckpointError("Checkpoint directory must be named checkpoint-<step>")
    return path


def _inventory(path: Path) -> dict:
    result = {}
    for item in sorted(path.rglob("*")):
        if item.is_symlink():
            raise CheckpointError("Checkpoint symlinks are not supported")
        if item.is_dir():
            continue
        if not item.is_file():
            raise CheckpointError("Checkpoint contains a non-regular file")
        relative = item.relative_to(path).as_posix()
        if relative == MANIFEST_NAME:
            continue
        if any(part.startswith(".") for part in item.relative_to(path).parts):
            raise CheckpointError("Checkpoint contains a temporary/hidden file")
        size = item.stat().st_size
        if size == 0:
            raise CheckpointError(f"Empty checkpoint file: {relative}")
        result[relative] = {"bytes": size, "sha256": sha256_file(item)}
    for name in REQUIRED_FILES:
        if name not in result:
            raise CheckpointError(f"Incomplete resume checkpoint: missing {name}")
    if not any(name in result for name in ("adapter_model.safetensors", "adapter_model.bin")):
        raise CheckpointError("Incomplete resume checkpoint: missing adapter weights")
    return result


def _step(path: Path) -> int:
    try:
        state = json.loads((path / "trainer_state.json").read_text())
    except (OSError, ValueError) as error:
        raise CheckpointError("Invalid trainer_state.json") from error
    if not isinstance(state, dict):
        raise CheckpointError("trainer_state.json must contain an object")
    step = state.get("global_step")
    if isinstance(step, bool) or not isinstance(step, int) or step <= 0:
        raise CheckpointError("Checkpoint must follow a completed optimizer step")
    if path.name != f"checkpoint-{step}":
        raise CheckpointError("Directory name and trainer global_step disagree")
    return step


def verify_checkpoint(checkpoint_dir, expected_metadata=None) -> dict:
    """Verify every saved file and compatibility metadata without deserializing tensors."""
    path = _checkpoint_dir(checkpoint_dir)
    manifest_path = path / MANIFEST_NAME
    if manifest_path.is_symlink():
        raise CheckpointError("Checkpoint manifest cannot be a symlink")
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, ValueError) as error:
        raise CheckpointError("Missing/invalid complete checkpoint manifest") from error
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1 or manifest.get("status") != "COMPLETE":
        raise CheckpointError("Checkpoint has not been published as complete")
    metadata = _metadata(manifest.get("metadata"))
    for key, expected in (expected_metadata or {}).items():
        if metadata.get(key) != expected:
            raise CheckpointError(f"Resume metadata mismatch: {key}")
    if manifest.get("files") != _inventory(path):
        raise CheckpointError("Checkpoint file inventory/hash mismatch")
    if manifest.get("global_step") != _step(path):
        raise CheckpointError("Checkpoint global_step mismatch")
    return manifest


def publish_checkpoint(checkpoint_dir, metadata, commit=None) -> dict:
    """Publish after Trainer finishes saving. commit is e.g. modal_volume.commit.

    Persist payload+manifest first, then replace and persist latest.json. A failed
    first commit leaves the previous latest pointer unchanged. Never call while
    another thread is still saving into this directory.
    """
    path = _checkpoint_dir(checkpoint_dir)
    metadata = _metadata(metadata)
    manifest_path = path / MANIFEST_NAME
    if manifest_path.exists():
        manifest = verify_checkpoint(path, metadata)
    else:
        inventory = _inventory(path)
        manifest = {
            "schema_version": 1, "status": "COMPLETE",
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "global_step": _step(path), "metadata": metadata, "files": inventory,
        }
        _atomic_json(manifest_path, manifest)
        verify_checkpoint(path, metadata)
    if commit:
        commit()
    _atomic_json(path.parent / LATEST_NAME, {
        "schema_version": 1, "checkpoint": path.name,
        "global_step": manifest["global_step"],
        "manifest_sha256": sha256_file(manifest_path),
    })
    if commit:
        commit()
    return manifest


def latest_checkpoint(run_dir, expected_metadata=None) -> Path | None:
    """Resolve only the committed latest pointer; do not guess from partial folders."""
    run = Path(run_dir)
    pointer_path = run / LATEST_NAME
    if not pointer_path.exists():
        return None
    if pointer_path.is_symlink():
        raise CheckpointError("Latest pointer cannot be a symlink")
    try:
        pointer = json.loads(pointer_path.read_text())
    except (OSError, ValueError) as error:
        raise CheckpointError("Invalid latest checkpoint pointer") from error
    if not isinstance(pointer, dict) or pointer.get("schema_version") != 1:
        raise CheckpointError("Invalid latest checkpoint pointer schema")
    name = pointer.get("checkpoint", "")
    if not isinstance(name, str) or not CHECKPOINT_NAME.fullmatch(name):
        raise CheckpointError("Unsafe checkpoint name in latest pointer")
    path = run / name
    manifest = verify_checkpoint(path, expected_metadata)
    if pointer.get("manifest_sha256") != sha256_file(path / MANIFEST_NAME):
        raise CheckpointError("Latest pointer manifest hash mismatch")
    if pointer.get("global_step") != manifest["global_step"]:
        raise CheckpointError("Latest pointer step mismatch")
    return path


def quarantine_unpublished_checkpoints(run_dir, expected_metadata=None, commit=None) -> list[Path]:
    """Move unfinished later saves aside before HF reuses their directory names.

    Call only when no writer is running. Renaming retains potentially useful
    partial work; it never turns an unpublished save into a resume candidate.
    """
    run = Path(run_dir)
    if not run.exists():
        return []
    latest = latest_checkpoint(run, expected_metadata)
    last_step = _step(latest) if latest else 0
    moved = []
    for path in sorted(run.iterdir()):
        if not CHECKPOINT_NAME.fullmatch(path.name):
            continue
        if path.is_symlink() or not path.is_dir():
            raise CheckpointError("Unexpected checkpoint path while recovering a run")
        if int(path.name.removeprefix("checkpoint-")) <= last_step:
            continue
        quarantine = run / ".unpublished"
        quarantine.mkdir(exist_ok=True)
        target = quarantine / f"{path.name}-{uuid.uuid4().hex}"
        os.replace(path, target)
        moved.append(target)
    if moved and commit:
        commit()
    return moved


def export_checkpoint(checkpoint_dir, archive_path, expected_metadata=None) -> Path:
    """Export a verified checkpoint as a ZIP without following symlinks."""
    source = _checkpoint_dir(checkpoint_dir)
    verify_checkpoint(source, expected_metadata)
    destination = Path(archive_path)
    if destination.exists():
        raise CheckpointError("Refusing to overwrite an existing checkpoint export")
    if source.resolve() in destination.resolve().parents:
        raise CheckpointError("Export destination cannot be inside the checkpoint")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".checkpoint-export-", dir=destination.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED) as archive:
            for item in sorted(source.rglob("*")):
                if item.is_file():
                    archive.write(item, f"{source.name}/{item.relative_to(source).as_posix()}")
        verify_checkpoint(source, expected_metadata)
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return destination


def import_checkpoint(archive_path, destination_root, expected_metadata=None,
                      commit=None, max_bytes=16 * 1024**3) -> Path:
    """Extract into staging, verify hashes, then publish; never overwrite a run."""
    destination = Path(destination_root)
    destination.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".checkpoint-import-", dir=destination))
    try:
        with zipfile.ZipFile(archive_path) as archive:
            members = archive.infolist()
            if not members or len(members) > 10000 or sum(m.file_size for m in members) > max_bytes:
                raise CheckpointError("Checkpoint archive exceeds import limits")
            roots, seen = set(), set()
            for member in members:
                name = member.filename
                relative = PurePosixPath(name)
                if ("\\" in name or relative.is_absolute() or
                        any(p in ("", ".", "..") for p in name.split("/")) or
                        len(relative.parts) < 2 or
                        not CHECKPOINT_NAME.fullmatch(relative.parts[0])):
                    raise CheckpointError("Unsafe path in checkpoint archive")
                if name in seen or member.is_dir():
                    raise CheckpointError("Duplicate/directory entries are not supported")
                seen.add(name)
                mode = member.external_attr >> 16
                if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG)):
                    raise CheckpointError("Archive contains a non-regular entry")
                roots.add(relative.parts[0])
                if len(roots) != 1:
                    raise CheckpointError("Archive must contain one checkpoint")
                target = staging.joinpath(*relative.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member) as incoming, target.open("xb") as outgoing:
                    shutil.copyfileobj(incoming, outgoing, length=1024 * 1024)
        name = roots.pop()
        staged = staging / name
        manifest = verify_checkpoint(staged, expected_metadata)
        target = destination / name
        if target.exists() or target.is_symlink():
            raise CheckpointError("Refusing to overwrite an existing checkpoint")
        os.replace(staged, target)
        publish_checkpoint(target, manifest["metadata"], commit)
        return target
    finally:
        shutil.rmtree(staging, ignore_errors=True)
