import os
import sys
import json
import anthropic

def run_looping_engine(task_description: str):
    """Executes the Looping Engine via Anthropic API with 4-phase self-correction."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[!] Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    skill_path = ".claude/skills/looping-engine/SKILL.md"

    if not os.path.exists(skill_path):
        print(f"[!] Error: Skill file not found at {skill_path}")
        sys.exit(1)

    with open(skill_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    print(f"[*] Dispatching Task to Looping Engine v1.3...\nTask: {task_description}\n")

    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": task_description}]
    )

    print("--- ENGINE OUTPUT ---\n")
    print(response.content[0].text)

if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "Design a hardware module buffering telemetry to SPI Flash with a 10ms hardware crypto-erase on physical tamper."
    run_looping_engine(task)
