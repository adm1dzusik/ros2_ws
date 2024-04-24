import subprocess

def get_video_index_by_model(model_name):
    try:
        output = subprocess.check_output("v4l2-ctl --list-devices", shell=True, stderr=subprocess.STDOUT)
        output_str = output.decode("utf-8")

        lines = output_str.split('\n')
        for i, line in enumerate(lines):
            if model_name in line:
                next_line = lines[i + 1]  # Переходимо до наступного рядка
                device_index = next_line.split("/dev/video")[-1]
                return device_index.strip()

    except subprocess.CalledProcessError as e:
        print("Mistake, when program is running to command:", e.output.decode("utf-8"))

    return None

if __name__ == "__main__":
    model_name = "Microsoft LifeCam"  # Замініть на бажану модель камери
    video_index = get_video_index_by_model(model_name)
    if video_index:
        print(f"Index of model '{model_name}': {video_index}")
    else:
        print(f"Video_device of model '{model_name}' not find.")







