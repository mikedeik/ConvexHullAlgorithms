from collections import deque


def bfs_traversal_from_index(lst, start_index):
    if not (0 <= start_index < len(lst)):
        return []

    visited = [False] * len(lst)
    result = []
    queue = deque()

    queue.append(start_index)
    visited[start_index] = True

    while queue:
        current_index = queue.popleft()
        result.append(lst[current_index])

        # Find neighbors (adjacent elements) and visit them
        for neighbor_index in [current_index - 1, current_index + 1]:
            if 0 <= neighbor_index < len(lst) and not visited[neighbor_index]:
                queue.append(neighbor_index)
                visited[neighbor_index] = True

    return result

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
start_index = 2  # Change this to the index you want to start from

result = bfs_traversal_from_index(my_list, start_index)
print(result)