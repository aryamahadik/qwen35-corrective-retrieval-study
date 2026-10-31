"""Aggregate completed per-verifier results without name collisions or empty success.

The environment runner must supply one result for every original verifier index.
This utility does not execute SQL or replace a missing enterprise backend.
"""
class VerifierResultError(ValueError): pass

def strict_task_success(task, outcomes, *, quality_holds=()):
    if task['task_id'] in set(quality_holds):
        raise VerifierResultError('Task has an unresolved scorer-quality hold')
    expected=task.get('verifiers')
    if not isinstance(expected,list) or not expected:
        raise VerifierResultError('A task must have at least one required verifier')
    by_index={}
    for row in outcomes:
        index=row.get('verifier_index')
        if type(index) is not int or not 0<=index<len(expected) or index in by_index:
            raise VerifierResultError('Invalid or duplicate verifier result index')
        if type(row.get('passed')) is not bool:
            raise VerifierResultError('Every verifier must have an explicit boolean result')
        by_index[index]=row
    if set(by_index)!=set(range(len(expected))):
        raise VerifierResultError('Required verifier outcomes are missing; cannot declare success')
    return all(by_index[i]['passed'] and not by_index[i].get('error') for i in range(len(expected)))
