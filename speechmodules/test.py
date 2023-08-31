def check_goodbye(q):
    if "再见" in q or "拜拜" in q:
        return True
    return False

def main():
    text = input("请输入一段文字: ")
    if check_goodbye(text):
        print("再见")
    else:
        print("没有发现再见或拜拜")

if __name__ == "__main__":
    main()
