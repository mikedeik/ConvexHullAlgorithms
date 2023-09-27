import imageio

# Collect all saved image files into a list
frames = [f'imageFrames/frame_{i:04d}.png' for i in range(98)]

# Create the GIF
with imageio.get_writer('convex_hull_animation.gif', mode='I', duration=0.5) as writer:
    for frame in frames:
        image = imageio.imread(frame)
        writer.append_data(image)
