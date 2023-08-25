import pandas as pd
import re

def compare_version(vcpkg_version_df, upstream_version_df):

    vcpkg_version_df["Update"] = ''

    #backup

    vcpkg_version_df = vcpkg_version_df.copy()
    upstream_version_df = upstream_version_df.copy()
    print(vcpkg_version_df)
    print(upstream_version_df)
    for index, row in vcpkg_version_df.iterrows():

        #获取version 和 upstream_version 列的值
        version = row["Version"]
        upstream_version = row["Upstream_version"]

        #Boost, QT集中处理
        name = row["Name"]
        if name == "boost" or name.startswith("boost-"):
            if upstream_version in upstream_version_df["Version"].values:
                vcpkg_version_df.at[index, "Upstream_version"] = version
                vcpkg_version_df.at[index, "Update"] = True

        elif name == "qt5" or name.startswith("qt5-"):
            if upstream_version in upstream_version_df["Version"].values:
                vcpkg_version_df.at[index, "Upstream_version"] = version
                vcpkg_version_df.at[index, "Update"] = True

        elif name == "qt" or name.startswith("qt"):
            if upstream_version in upstream_version_df["Version"].values:
                vcpkg_version_df.at[index, "Upstream_version"] = version
                vcpkg_version_df.at[index, "Update"] = True

        elif name.startswith("kf5"):
            if upstream_version in upstream_version_df["Version"].values:
                vcpkg_version_df.at[index, "Upstream_version"] = version
                vcpkg_version_df.at[index, "Update"] = True


        #针对Version前缀集中处理'v'
        #正则比较
        pattern = r"^(v|V)?(.*)$"
        
        if upstream_version:
            match = re.match(pattern, upstream_version)
            if match:
                vcpkg_version_df.at[index, "Upstream_version"] = version
                vcpkg_version_df.at[index, "Update"] = True
            else:
                vcpkg_version_df.at[index, "Update"] = False
        else:
            vcpkg_version_df.at[index, "Update"] = False

    return vcpkg_version_df, upstream_version_df