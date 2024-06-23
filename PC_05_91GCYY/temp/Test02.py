from concurrent.futures import ThreadPoolExecutor, Future
import time

# 设置一个全局标志来指示是否应终止所有任务
should_stop = False


def worker(num: int, return_dict: dict) -> None:
    """thread worker function"""
    global should_stop
    try:
        print(f"Worker: {num}, started at {time.strftime('%X')}")
        time.sleep(2)  # 模拟耗时操作

        # 模拟任务可能失败的情况
        if num == 2:  # 假设第2个任务会“失败”
            raise ValueError("Simulated task failure")

        print(f"Worker: {num}, finished at {time.strftime('%X')}")
        return_dict[num] = 'Success'
    except Exception as e:
        print(f"Worker: {num}, encountered error: {e}")
        should_stop = True
        return_dict[num] = 'Failed'


def check_and_abort(future: Future):
    """Callback to check result and potentially stop other tasks."""
    global should_stop
    if future.result() == 'Failed':
        should_stop = True
        print("Detected a failed task, setting should_stop to True.")


# 使用ThreadPoolExecutor创建线程池
with ThreadPoolExecutor(max_workers=5) as executor:
    # 使用一个字典来收集每个任务的结果
    results = {}
    # 提交任务到线程池，并注册回调函数
    futures = {executor.submit(worker, i, results): i for i in range(5)}

    # 为每个任务添加完成时的回调，用于检查是否应终止
    for future in futures:
        future.add_done_callback(check_and_abort)

    # 等待所有任务完成，但可以根据should_stop调整逻辑
    for future in futures:
        future.result()  # 这里简单等待结果，实际可根据should_stop调整

    # 检查是否所有任务都因失败而停止
    if should_stop:
        print("Some tasks failed, stopping the execution.")
    else:
        print("All tasks completed successfully.")

print("Processing complete.")