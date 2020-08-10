import speech_recognition as sr
import requests
import click

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def post_line_notify(message, token, img_path=""):
    # 諸々の設定
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    # メッセージ
    payload = {"message": message}
    # 画像を含むか否か
    if img_path == "":
        res = requests.post(line_notify_api, data=payload, headers=headers)
        return res

    # 画像
    files = {"imageFile": open(img_path, "rb")}
    res = requests.post(line_notify_api, data=payload, headers=headers, files=files)
    return res

@click.command()
@click.option('-t', '--token', 'token')
def main(token):
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=0)

    while True:
        print("Say something ...")

        with mic as source:
            r.adjust_for_ambient_noise(source) #雑音対策
            audio = r.listen(source)

        print ("Now to recognize it...")

        try:
            message = r.recognize_google(audio, language='ja-JP')
            print(message)
            if "かずくん" in message:
                res = post_line_notify(message,token)
                print(f"line通知<{res}>")

        # 以下は認識できなかったときに止まらないように。
        except sr.UnknownValueError:
            print("could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    main()