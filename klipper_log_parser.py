import re
import argparse
import pandas as pd

# エラーパターンを定義
error_patterns = {
    "temperature": r"Error: Heater failed",
    "motor": r"Error: Stepper driver not responding",
    "timeout": r"Timeout error",
    "communication": r"Communication failed",
}

# エラーログ解析
def parse_log(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    errors = []
    for line in lines:
        for error_type, pattern in error_patterns.items():
            if re.search(pattern, line):
                timestamp = line.split(" ")[0]  # タイムスタンプを取得
                errors.append({"timestamp": timestamp, "error_type": error_type, "message": line.strip()})
    
    return errors

# レポート生成
def generate_report(errors):
    if errors:
        df = pd.DataFrame(errors)
        df.to_csv("error_report.csv", index=False)
        print("エラーレポートが 'error_report.csv' として生成されました。")
    else:
        print("エラーは検出されませんでした。")

# コマンドライン引数の設定
def main():
    parser = argparse.ArgumentParser(description="Klipperログ解析ツール")
    parser.add_argument("log_file", help="解析するKlipperログファイルのパス")
    args = parser.parse_args()

    errors = parse_log(args.log_file)
    generate_report(errors)

if __name__ == "__main__":
    main()
