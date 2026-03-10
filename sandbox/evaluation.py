import json
import subprocess
import tempfile
import os
import shutil
import uuid
import re


# ==============================
# Clean Model Code
# ==============================

def clean_code(code):
    code = code.strip()

    if code.startswith("```"):
        code = re.sub(r"^```[a-zA-Z]*", "", code)
        code = code.rstrip("```")

    return code.strip()


# ==============================
# Docker Execution
# ==============================

def run_in_docker(code, input_data, problem_data):

    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "solution.py")

    cleaned_code = clean_code(code)

    with open(file_path, "w") as f:
        f.write(cleaned_code)

    container_name = f"eval_{uuid.uuid4().hex}"

    time_limit_sec = problem_data.get("time_limit_ms", 2000) / 1000
    memory_limit_kb = problem_data.get("memory_limit_kb", 262144)

    try:
        command = [
            "docker", "run",
            "--rm",
            "-i",                         # IMPORTANT: keep stdin open
            "--name", container_name,
            "--memory", f"{memory_limit_kb}k",
            "--network", "none",
            "-v", f"{temp_dir}:/app",
            "python:3.10",
            "bash", "-c",
            f"timeout {time_limit_sec}s python /app/solution.py"
        ]

        process = subprocess.run(
            command,
            input=input_data,             # feed input here
            text=True,
            capture_output=True
        )

        if process.returncode == 124:
            return {"status": "tle", "result": ""}

        if process.returncode != 0:
            return {
                "status": "re",
                "result": process.stderr.strip()
            }

        return {
            "status": "ok",
            "result": process.stdout.strip()
        }

    except Exception as e:
        return {"status": "re", "result": str(e)}

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================
# Evaluate Single Problem
# ==============================

def evaluate_problem(problem_data, dataset_lookup):

    problem_name = problem_data["name"]
    student_code = problem_data["generated_code"]

    dataset_info = dataset_lookup.get(problem_name, {})

    tests = problem_data.get("tests", [])
    total_tests = len(tests)

    passed = wa = tle = re_count = 0

    print(f"\n=== {problem_name} ===")

    for index, test in enumerate(tests):

        response = run_in_docker(
            student_code,
            test["input"],
            dataset_info
        )

        # 🔴 If Runtime Error → terminate immediately
        if response["status"] == "re":
            print("Runtime Error:")
            print(response["result"])

            re_count = total_tests
            passed = 0
            wa = 0
            tle = 0

            print(f"Score: 0/{total_tests}")
            print(f"WA: 0 | TLE: 0 | RE: {total_tests}")

            return {
                "passed": 0,
                "total": total_tests,
                "wa": 0,
                "tle": 0,
                "re": total_tests
            }

        expected = str(test["output"]).strip()
        actual = str(response["result"]).strip()

        if response["status"] == "ok":
            if actual == expected:
                passed += 1
            else:
                wa += 1

        elif response["status"] == "tle":
            tle += 1

    print(f"Score: {passed}/{total_tests}")
    print(f"WA: {wa} | TLE: {tle} | RE: {re_count}")

    return {
        "passed": passed,
        "total": total_tests,
        "wa": wa,
        "tle": tle,
        "re": re_count
    }
# ==============================
# Main
# ==============================

def main():

    with open("codecontests_bell_200.json", "r") as f:
        dataset = json.load(f)

    dataset_lookup = {
        problem["name"]: problem
        for problem in dataset
    }

    with open("generated_results.json", "r") as f:
        problems = json.load(f)

    overall_passed = 0
    overall_total = 0
    overall_wa = 0
    overall_tle = 0
    overall_re = 0

    for problem in problems:
        result = evaluate_problem(problem, dataset_lookup)

        overall_passed += result["passed"]
        overall_total += result["total"]
        overall_wa += result["wa"]
        overall_tle += result["tle"]
        overall_re += result["re"]

    print("\n==============================")
    print("FINAL RESULT")
    print("==============================")
    print(f"Total Score: {overall_passed}/{overall_total}")

    if overall_total > 0:
        accuracy = (overall_passed / overall_total) * 100
        print(f"Accuracy: {accuracy:.2f}%")

    print(f"Total WA: {overall_wa}")
    print(f"Total TLE: {overall_tle}")
    print(f"Total RE: {overall_re}")
    print("==============================")


if __name__ == "__main__":
    main()