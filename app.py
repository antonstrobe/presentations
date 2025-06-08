import os
import json
import threading
from tkinter import Tk, Entry, Button, Label, PhotoImage, messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import openai
from io import BytesIO
import base64

CONFIG_FILE = 'openai_key.txt'


def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return f.read().strip()
    return None


def save_api_key(key):
    with open(CONFIG_FILE, 'w') as f:
        f.write(key)


def request_api_key(root):
    key = filedialog.askstring('API Key', 'Enter your OpenAI API key:')
    if key:
        save_api_key(key)
        return key
    else:
        messagebox.showerror('Error', 'API key is required to continue.')
        root.destroy()
        return None


def get_description(query):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                'content': (
                    'You are an assistant that returns JSON for image, audio and video. '
                    'Given a user query, respond ONLY with a JSON like:\n'
                    '{"image_prompt": "text for image", '
                    '"audio_text": "text to speak", '
                    '"video_prompt": "text for video"}'
                )
            },
            {'role': 'user', 'content': query}
        ]
    )
    content = response['choices'][0]['message']['content']
    return json.loads(content)


def generate_image(prompt):
    img_resp = openai.Image.create(prompt=prompt, n=1, size='512x512', response_format='b64_json')
    b64_data = img_resp['data'][0]['b64_json']
    return Image.open(BytesIO(base64.b64decode(b64_data)))


def generate_audio(text, file_path):
    speech_resp = openai.audio.speech.create(model='tts-1', voice='alloy', input=text)
    with open(file_path, 'wb') as f:
        f.write(speech_resp.content)


def generate_video(image_path, audio_path, output_path):
    try:
        from moviepy.editor import ImageClip, AudioFileClip
        clip = ImageClip(image_path).set_duration(5)
        clip = clip.set_audio(AudioFileClip(audio_path))
        clip.write_videofile(output_path, codec='libx264', fps=24)
    except Exception as e:
        print('Video generation failed:', e)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Mini Presentation')
        self.entry = Entry(root, width=50)
        self.entry.pack(pady=10)
        self.button = Button(root, text='Send', command=self.process)
        self.button.pack()
        self.progress = ttk.Label(root, text='')
        self.progress.pack(pady=5)
        self.image_label = Label(root)
        self.image_label.pack(pady=5)
        self.audio_button = Button(root, text='Play Audio', command=self.play_audio, state='disabled')
        self.audio_button.pack(pady=5)
        self.video_button = Button(root, text='Open Video', command=self.open_video, state='disabled')
        self.video_button.pack(pady=5)
        self.audio_file = None
        self.video_file = None

    def process(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showinfo('Input required', 'Please enter a word or phrase.')
            return
        threading.Thread(target=self.run_workflow, args=(query,), daemon=True).start()

    def run_workflow(self, query):
        self.update_status('Generating description...')
        try:
            desc = get_description(query)
        except Exception as e:
            self.update_status('Error getting description')
            messagebox.showerror('Error', f'Failed to get description: {e}')
            return

        # Image
        self.update_status('Generating image...')
        try:
            img = generate_image(desc['image_prompt'])
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            self.update_status('Error generating image')
            messagebox.showerror('Error', f'Failed to generate image: {e}')
            return

        # Audio
        self.update_status('Generating audio...')
        try:
            self.audio_file = 'speech.mp3'
            generate_audio(desc['audio_text'], self.audio_file)
            self.audio_button.config(state='normal')
        except Exception as e:
            self.update_status('Error generating audio')
            messagebox.showerror('Error', f'Failed to generate audio: {e}')
            return

        # Video
        self.update_status('Generating video...')
        try:
            self.video_file = 'video.mp4'
            img.save('frame.png')
            generate_video('frame.png', self.audio_file, self.video_file)
            self.video_button.config(state='normal')
        except Exception as e:
            self.update_status('Video generation failed')
            messagebox.showwarning('Warning', f'Video generation failed: {e}')

        self.update_status('Done!')

    def play_audio(self):
        if self.audio_file:
            try:
                import webbrowser
                webbrowser.open(self.audio_file)
            except Exception as e:
                messagebox.showerror('Error', f'Cannot play audio: {e}')

    def open_video(self):
        if self.video_file:
            try:
                import webbrowser
                webbrowser.open(self.video_file)
            except Exception as e:
                messagebox.showerror('Error', f'Cannot open video: {e}')

    def update_status(self, text):
        self.progress.config(text=text)


def main():
    root = Tk()
    api_key = load_api_key()
    if not api_key:
        api_key = request_api_key(root)
    if not api_key:
        return
    openai.api_key = api_key
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
