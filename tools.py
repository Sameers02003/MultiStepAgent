from typing import Dict, Any
import re

# --- Time helpers ---
def _time_to_minutes(t: str) -> int:
    if not t or len(t) < 5 or ":" not in t:
        raise ValueError(f"Invalid time format: '{t}'")
    parts = t.split(":")
    return int(parts[0]) * 60 + int(parts[1])

def _format_duration(mins: int) -> str:
    h = mins // 60
    m = mins % 60
    return f"{h} hours {m} minutes" if h else f"{m} minutes"

def _extract_times(question: str):
    return re.findall(r'\b([01]?\d|2[0-3]):[0-5]\d\b', question)

# --- Problem solvers ---
def solve_time_difference(question: str) -> Dict[str, Any]:
    times = _extract_times(question)
    if len(times) >= 2:
        try:
            start = _time_to_minutes(times[0])
            end = _time_to_minutes(times[1])
            if end >= start:
                diff = end - start
                return {
                    "answer": _format_duration(diff),
                    "reasoning": f"Time difference between {times[0]} and {times[1]} is {diff} minutes."
                }
        except ValueError as e:
            return {"answer": "", "reasoning": str(e)}
    return {}

def solve_apples(question: str) -> Dict[str, Any]:
    nums = [int(x) for x in re.findall(r'\d+', question)]
    if nums:
        red = nums[0]
        if "twice" in question.lower():
            green = 2 * red
            total = red + green
            return {
                "answer": str(total),
                "reasoning": f"Red={red}, Green={green}, Total={total}."
            }
    return {}

def solve_meeting(question: str) -> Dict[str, Any]:
    m = re.search(r'need\s+(\d+)\s+minutes', question.lower())
    if not m:
        return {}
    need = int(m.group(1))
    slots = re.findall(r'([01]?\d|2[0-3]):[0-5]\d[–-]([01]?\d|2[0-3]):[0-5]\d', question)
    fits = []
    for s, e in slots:
        try:
            s_m = _time_to_minutes(s)
            e_m = _time_to_minutes(e)
            dur = e_m - s_m
            if dur >= need:
                fits.append(f"{s}–{e}")
        except ValueError:
            continue
    if fits:
        return {
            "answer": ", ".join(fits),
            "reasoning": f"Slots with duration ≥ {need} minutes: {', '.join(fits)}."
        }
    return {"answer": "", "reasoning": f"No slot fits {need} minutes."}

def solve_with_tools(question: str, steps) -> Dict[str, Any]:
    ql = question.lower()
    if "train" in ql or "arrive" in ql or "depart" in ql:
        r = solve_time_difference(question)
        if r: return r
    if "apples" in ql:
        r = solve_apples(question)
        if r: return r
    if "slot" in ql or "minutes" in ql:
        r = solve_meeting(question)
        if r: return r
    m = re.search(r'(-?\d+)\s*\+\s*(-?\d+)', ql)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        s = a + b
        return {"answer": str(s), "reasoning": f"Computed {a} + {b} = {s}."}
    return {}

# --- Constraint verifier ---
def verify_constraints(question: str, proposal: Dict[str, Any]) -> Dict[str, Any]:
    ans = proposal.get("answer")
    if ans is None or (isinstance(ans, str) and ans.strip() == ""):
        return {"passed": False, "details": "Missing or empty answer."}
    times = _extract_times(question)
    if len(times) >= 2 and ("hour" in ans or "minute" in ans):
        try:
            start = _time_to_minutes(times[0])
            end = _time_to_minutes(times[1])
            if end < start:
                return {"passed": False, "details": "Arrival before departure."}
        except ValueError as e:
            return {"passed": False, "details": str(e)}
    return {"passed": True, "details": "Constraints OK."}