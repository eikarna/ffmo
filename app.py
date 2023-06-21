import os
from ffmpy import FFmpeg
import gradio as gr
import subprocess
import shortuuid
from tempfile import _TemporaryFileWrapper

# Check Runtime to avoid Error
globalopt = []
limit = os.getenv("SYSTEM") == "spaces"
if limit:
    globalopt = ["-y", "-hide_banner", "-threads 64", "-filter_threads 64", "-filter_complex_threads 64"]
else:
    globalopt = ["-y", "-hide_banner", "-hwaccel cuda", "-threads 64", "-filter_threads 64", "-filter_complex_threads 64"]

# Function to process data
def convert(file: _TemporaryFileWrapper, options: str):
    output_file=""
    video=""
    stdout=""
    ffmpeg=FFmpeg()
    print(file)
    print(options)
    try:
        output_file = f"{shortuuid.ShortUUID().random(length=8)}.mp4"
        ffmpeg = FFmpeg(inputs={file: None}, outputs={output_file: f"{options}"}, global_options=globalopt)
        ffmpeg.run(stderr=subprocess.PIPE)
        # pprint(f"{stdout} {stderr}")
        stdout += f"{ffmpeg.cmd}"
        gr.Textbox.update(value=stdout)
        gr.Video.update(value=output_file)

    except Exception as e:
        stderr=e
        stdout += f"{stderr}"
    return [stdout, output_file]

# Command Builder: Smooth Interpolation
def cmdb_si(a, b, c):
    tuning = c.split(" –")[0]
    # print(tuning)
    return f"-filter:v \"minterpolate='mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:fps={a}'\" -r {a} -preset {b} -tune {tuning}"

# Command Builder: Frame Blending
def cmdb_fb(a, b, c):
    tuning = c.split(" –")[0]
    # print(tuning)
    return f"-filter:v \"tblend\" -r {a} -preset {b} -tune {tuning}"

# Command Builder: Advanced
def cmdb_adv(a, b):
    tuning = b.split(" –")[0]
    gr.Textbox.update(value=f"-preset {a} -tune {b}")
    # return f"-preset {a} -tune {b}"

with gr.Blocks(title="FFmo - FFmpeg Online", theme=gr.themes.Soft()) as main:
    with gr.Tabs():
        with gr.TabItem("Smooth Interpolation"):
            with gr.Row():
                with gr.Column() as inp_si:
                    input_fps = gr.Slider(1, 144, value=60, label="Frame Per Second (FPS)", info="Choose between 1 and 144 Fps")
                    input_preset = gr.Dropdown(["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"], value=["veryslow"], label="Preset (Required)", info="Semakin lama (slow), semakin bagus hasilnya.")
                    input_tune = gr.Radio(["film – use for high quality movie content; lowers deblocking", "animation – good for cartoons; uses higher deblocking and more reference frames", "grain – preserves the grain structure in old, grainy film material", "stillimage – good for slideshow-like content", "fastdecode – allows faster decoding by disabling certain filters", "zerolatency – good for fast encoding and low-latency streaming", "psnr – ignore this as it is only used for codec development", "ssim – ignore this as it is only used for codec development"], value=["film – use for high quality movie content; lowers deblocking"], label="Tune (Required)", info="Tuning Setting")
                    input_video = gr.Video(label="Input Video")
                    input_textbox = gr.Textbox(label="FFMPEG Command")

                with gr.Column() as out_si:
                    output_textbox = gr.Textbox(label="Output Logs", interactive=False)
                    output_video = gr.Video(label="Output Video", interactive=False)
                    buildcmd = gr.Button("Build FFMPEG Command", variant="primary").click(fn=cmdb_si, inputs=[input_fps,input_preset,input_tune], outputs=[input_textbox])
                startconv = gr.Button("Start", variant="primary").click(fn=convert, inputs=[input_video,input_textbox], outputs=[output_textbox, output_video])
                clear_button = gr.ClearButton([input_fps, input_preset, input_tune, input_video, input_textbox, output_textbox, output_video])
        
        with gr.TabItem("Frame Blending"):
            with gr.Row():
                with gr.Column() as inp_fb:
                    input_fps2 = gr.Slider(1, 144, value=60, label="Frame Per Second (FPS)", info="Choose between 1 and 144 Fps")
                    input_preset2 = gr.Dropdown(["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"], value=["veryslow"], label="Preset (Required)", info="Semakin lama (slow), semakin bagus hasilnya.")
                    input_tune2 = gr.Radio(["film – use for high quality movie content; lowers deblocking", "animation – good for cartoons; uses higher deblocking and more reference frames", "grain – preserves the grain structure in old, grainy film material", "stillimage – good for slideshow-like content", "fastdecode – allows faster decoding by disabling certain filters", "zerolatency – good for fast encoding and low-latency streaming", "psnr – ignore this as it is only used for codec development", "ssim – ignore this as it is only used for codec development"], value=["film – use for high quality movie content; lowers deblocking"], label="Tune (Required)", info="Tuning Setting")
                    input_video2 = gr.Video(label="Input Video")
                    input_textbox2 = gr.Textbox(label="FFMPEG Command")

                with gr.Column() as out_fb:
                    output_textbox2 = gr.Textbox(label="Output Logs", interactive=False)
                    output_video2 = gr.Video(label="Output Video", interactive=False)
                    buildcmd2 = gr.Button("Build FFMPEG Command", variant="primary").click(fn=cmdb_fb, inputs=[input_fps2,input_preset2,input_tune2], outputs=[input_textbox2])
                startconv2 = gr.Button("Start", variant="primary").click(fn=convert, inputs=[input_video2,input_textbox2], outputs=[output_textbox2, output_video2])
                clear_button2 = gr.ClearButton([input_fps2, input_preset2, input_tune2, input_video2, input_textbox2, output_textbox2, output_video2])

        with gr.TabItem("Advanced"):
            with gr.Row():
                with gr.Column() as inp_main:
                    input_preset3 = gr.Dropdown(["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"], value=["veryslow"], label="Preset (Required)", info="Semakin lama (slow), semakin bagus hasilnya.")
                    input_tune3 = gr.Radio(["film – use for high quality movie content; lowers deblocking", "animation – good for cartoons; uses higher deblocking and more reference frames", "grain – preserves the grain structure in old, grainy film material", "stillimage – good for slideshow-like content", "fastdecode – allows faster decoding by disabling certain filters", "zerolatency – good for fast encoding and low-latency streaming", "psnr – ignore this as it is only used for codec development", "ssim – ignore this as it is only used for codec development"], value=["film – use for high quality movie content; lowers deblocking"], label="Tune (Required)", info="Tuning Setting")
                    input_textbox3 = gr.Textbox(label="FFMPEG Command")
                    input_video3 = gr.Video(label="Input Video")
                    buildcmd = gr.Button("Build FFMPEG Command", variant="primary").click(fn=cmdb_adv, inputs=[input_preset3,input_tune3], outputs=[input_textbox3])
                with gr.Column() as out_main:
                    output_textbox3 = gr.Textbox(label="Output Logs", interactive=False)
                    output_video3 = gr.Video(label="Output Video", interactive=False)
                startconv3 = gr.Button("Start", variant="primary").click(fn=convert, inputs=[input_video3,input_textbox3], outputs=[output_textbox3, output_video3])
                clear_button3 = gr.ClearButton([input_textbox3, input_video3, output_textbox3, output_video3])

# Launch the combined interface
if __name__ == "__main__":
    if limit:
        main.queue(concurrency_count=5).launch()
    else:
        main.queue(concurrency_count=5).launch(debug=True, share=True)
