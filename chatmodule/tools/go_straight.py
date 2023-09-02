"""机器人运动"""

import subprocess
import os


class GoStraitRun(object):
    name = "Go Strait"
    description = (
        "Useful for when you need to go strait"
    )

    def run(self, no_use: str) -> str:

        # 设置命令行命令和工作目录
        command = 'mvn test'
        working_directory = './testRobotMove'

        # 执行命令
        subprocess.call(command, cwd=working_directory, shell=True)



        return "直走成功"



if __name__ == '__main__':
    print(GoStraitRun().run(''))
