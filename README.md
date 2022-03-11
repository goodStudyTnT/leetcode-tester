# Leetcode Tester

> Leetcode 本地测试工具
> 

# 背景

由于 [leetcode](https://leetcode-cn.com/) 特别的输入设计，如果想要在本地进行测试的话，你需要额外编写一些代码，比如实例化 Solution 类，将输入作为参数，并且将输出与正确答案进行比较。虽然这减轻了手写 I/O 的负担，但也使得本地测试变得十分困难。

Leetcode 的输入设计和 TopCoder 的十分类似，熟悉 TopCoder 的用户可能对这个插件比较了解：[TZTester](https://community.topcoder.com/contest/classes/TZTester/TZTester.html) ，它能够解析测试用例并且生成测试代码，让你能够在本地进行测试，而这也是本插件打算做的事情。

# 用法

### 环境要求：

- python3

1. 克隆仓库

```bash
git clone git@github.com:goodStudyTnT/leetcode-tester.git
cd leetcode-tester
```

1. 下载依赖包

```bash
pip install -r requirements
```

1. 填写配置，配置路径为 ‘config/config.yaml’ 

```yaml
username:                                     # leetcode-cn.com 用户名
password:                                     # 密码
language: cpp                                 # 所用语言，当前支持 cpp
openURL: True                                 # 是否自动打开页面

contest_dir:                                  # 生成代码文件夹
contest_id: -1 # 0                            #比赛 id，大于 0 表示指定比赛 id，等于 0 表示即将到来的比赛，小于 0 表示过去的前 x 场比赛
contest_type: weekly # 0                      # 比赛类型, 当前支持周赛 weekly
```

当然你也可以在运行在命令行覆盖配置文件中的配置，如：

```bash
python main.py get --contest_id 223
```

1. 运行命令，生成测试代码

```bash
python main.py get [-h] [--username USERNAME] [--password PASSWORD]
                   [--language LANGUAGE] [--contest_dir CONTEST_DIR]
                   [--contest_id CONTEST_ID] [--contest_type CONTEST_TYPE]
                   [--openURL OPENURL]
```

比如，生成 contest 185 的代码，语言选择 cpp

```bash
python main.py get --contest_id 185 --language cpp
```

运行完毕后，会在指定目录下生成两个文件夹。

- `185`: contest 185 的所有测试代码。**注意：请勿改动 `problem.json` 中的内容**

    ![Untitled.png](https://s2.loli.net/2022/03/12/DYcdNZg32sj7WSi.png)
    

- `utils`: 测试依赖的一些代码。**注意：本文件夹只会生成一次，即第一次生成后之后就不会再改里面的内容了，所以用户可以在里面添加一些自己的测试函数或模板，比如 TreeNode 的按层遍历等等。**

    ![Untitled _2_.png](https://s2.loli.net/2022/03/12/vUxrSyqQt7YwFW5.png)
    
1. 在 `solution.h` 中编写代码，编写完毕后，运行 `main.cpp` 得到结果。

    ![Untitled _3_.png](https://s2.loli.net/2022/03/12/cFw6GQevxDy8H7z.png)
    
2. 提交代码，如果 wrong answer 后，拿到错误样例，可以将错误样例贴到题目测试代码所在文件夹中的 data 里面。**注意：贴入顺序为样例的输入输出。**

    ![Untitled _4_.png](https://s2.loli.net/2022/03/12/QFTJkyjEY6lLGDN.png)
    
    修改完 data 后，需要重新生成 `main.cpp`，执行命令.
    
    ```bash
    python main.py build_test
    ```
    
   **注意：命令路径一定要在题目测试代码路径下。** 执行完毕后，即可运行 main 函数进行测试。
    
# 免责声明
    
1. 此工具与 LeetCode 没有任何关系，关联，授权，支持，或以任何方式正式连接。
    
# TODO：
    
- [ ]  支持 python, java, go 的测试代码生成
- [ ]  支持春秋赛的测试代码生成
- [ ]  支持指定题目的测试代码生成