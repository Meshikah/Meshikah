"""Stable exit codes (docs/04-cli-mvp.md; reference CLI spec §9)."""

from enum import IntEnum


class Exit(IntEnum):
    OK = 0
    BLOCKING_CHECK_FAILED = 1
    INVALID_INPUT = 2
    NOT_A_REPOSITORY = 3
    CHECKPOINT_ORDER_OR_EVIDENCE = 4
    RECORD_INCONSISTENT = 5
    SENSITIVE_DATA = 6
    HUMAN_ONLY = 7
    POLICY_ASK = 10
    POLICY_DENY = 11
    NOT_IMPLEMENTED = 69
    INTERNAL_ERROR = 70
