import subprocess

def package_with_pyinstaller(vcpkg_version):
    try:
        subprocess.run(['pyinstaller', '--onefile','--name=vcpkg_version', vcpkg_version], check=True)
        print(f"Packaging {vcpkg_version} successful!!!!")
    except subprocess.CalledProcessError:
        print(f"Error packaging {vcpkg_version}")
    except Exception as e:
        print(f"Unexpected error:{e}")

if __name__ == '__main__':
        package_with_pyinstaller('main.py')