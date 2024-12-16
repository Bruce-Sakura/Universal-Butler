import subprocess


def get_installed_software():
    try:
        # 使用 PowerShell 执行命令
        command = 'powershell -Command "Get-WmiObject -Class Win32_Product | Select-Object -Property Name"'
        data = subprocess.check_output(command, shell=True, universal_newlines=True)

        # 分割返回的字符串并去除空行
        software_list = [line.strip() for line in data.split('\n') if line.strip()]

        return software_list

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running PowerShell: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


if __name__ == "__main__":
    installed_software = get_installed_software()

    if installed_software:
        print("已安装的软件：")
        for software in installed_software:
            print(software)
    else:
        print("未能获取已安装的软件列表。")
