from service.login import Login


def main():
    try:
        _ = Login()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
