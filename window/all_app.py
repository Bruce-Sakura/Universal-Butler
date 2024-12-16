import winreg
import subprocess
import os


def get_installed_software_registry(software_list):
    """从注册表获取已安装软件的名称和启动路径"""
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for reg_path in reg_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                try:
                    sub_key_name = winreg.EnumKey(reg_key, i)
                    sub_key = winreg.OpenKey(reg_key, sub_key_name)

                    # 获取软件名称和路径
                    try:
                        name = winreg.QueryValueEx(sub_key, "DisplayName")[0] if "DisplayName" in dict(
                            winreg.QueryValueEx(sub_key)) else None
                        path = winreg.QueryValueEx(sub_key, "InstallLocation")[0] if "InstallLocation" in dict(
                            winreg.QueryValueEx(sub_key)) else None
                        if name and path and os.path.isdir(path):
                            software_list.append({"name": name, "path": path})
                    except KeyError:
                        continue  # 捕获键值不存在的异常
                except Exception:
                    continue  # 跳过无法打开子键的情况
        except Exception:
            continue  # 跳过无法打开注册表路径的情况

    return software_list


def get_installed_software_common_dirs(software_list):
    """扫描常见目录下的软件"""
    common_dirs = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        r"D:\Program Files",
        r"D:\Program Files (x86)",
        os.path.expanduser(r"~\AppData\Local"),
        os.path.expanduser(r"~\AppData\Roaming"),
    ]

    for folder in common_dirs:
        if os.path.exists(folder):
            for subdir in os.listdir(folder):
                full_path = os.path.join(folder, subdir)
                if os.path.isdir(full_path):
                    # 查找 .exe 文件
                    try:
                        for file in os.listdir(full_path):
                            if file.endswith(".exe"):
                                software_list.append({"name": subdir, "path": os.path.join(full_path, file)})
                                break
                    except Exception:
                        continue
    return software_list


def start_program(program_path):
    """启动指定路径的程序"""
    try:
        subprocess.Popen(program_path)  # 使用 subprocess 启动程序
        print(f"程序启动: {program_path}")
    except Exception as e:
        print(f"启动程序失败: {e}")


if __name__ == "__main__":
    software_list = []

    # 从注册表获取已安装的软件
    # a = get_installed_software_registry(software_list)

    # 如果需要，也可以获取常见目录下的软件
    b = get_installed_software_common_dirs(software_list)

    # print(a)  # 打印从注册表获取的软件列表
    print(b)  # 打印从常见目录获取的软件列表

    # # 示例：启动第一个程序
    # if a:
    #     start_program(a[0]["path"])
