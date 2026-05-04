import os
from openai import OpenAI
import subprocess

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def analyze_code(code):
    prompt = f"""
你是一个资深代码评审工程师，请分析以下代码的问题：
1. Bug
2. 性能问题
3. 代码规范问题

代码：
{code}
"""
    return call_llm(prompt)

def fix_code(code, analysis):
    prompt = f"""
根据以下分析结果，修复代码：

分析：
{analysis}

原始代码：
{code}

请输出修复后的完整代码：
"""
    return call_llm(prompt)

def run_tests():
    try:
        result = subprocess.run(
            ["pytest"],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return str(e)

def run_pipeline(file_path):
    with open(file_path, "r") as f:
        code = f.read()

    print("🔍 分析代码...")
    analysis = analyze_code(code)
    print(analysis)

    print("\n🛠 修复代码...")
    fixed_code = fix_code(code, analysis)

    fixed_path = file_path.replace(".py", "_fixed.py")
    with open(fixed_path, "w") as f:
        f.write(fixed_code)

    print(f"修复代码已保存到: {fixed_path}")

    print("\n🧪 运行测试...")
    test_result = run_tests()
    print(test_result)

if __name__ == "__main__":
    run_pipeline("example.py")
