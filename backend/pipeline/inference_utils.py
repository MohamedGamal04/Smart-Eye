from backend.pipeline.analyzer import merge_results
from backend.pipeline.rule_engine import evaluate_rules


def build_state(detection_results, camera_id, evaluate_rule_triggers=True):
    if not evaluate_rule_triggers:
        return merge_results(detection_results, camera_id), []

    state = merge_results(detection_results, camera_id)
    return state, evaluate_rules(state, camera_id)
