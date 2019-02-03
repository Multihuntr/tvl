import PIL.Image
import numpy as np
import pytest

from tvl_backends.pyav import PyAvBackendFactory


def test_pyav_read_frame(video_filename, first_frame_image):
    backend = PyAvBackendFactory().create(video_filename, 'cpu')
    rgb = backend.read_frame()

    assert(rgb.size() == (3, 720, 1280))

    rgb_bytes = (rgb * 255).round_().byte().cpu()
    img = PIL.Image.fromarray(rgb_bytes.permute(1, 2, 0).numpy(), 'RGB')

    np.testing.assert_allclose(img, first_frame_image, rtol=0, atol=50)


def test_pyav_eof(video_filename):
    backend = PyAvBackendFactory().create(video_filename, 'cpu')
    backend.seek(2.0)
    with pytest.raises(EOFError):
        backend.read_frame()


def test_pyav_read_all_frames(video_filename):
    backend = PyAvBackendFactory().create(video_filename, 'cpu')

    n_read = 0
    for i in range(1000):
        try:
            backend.read_frame()
            n_read += 1
        except EOFError:
            break
    assert n_read == 50


def test_pyav_seek(video_filename, mid_frame_image):
    backend = PyAvBackendFactory().create(video_filename, 'cpu')
    backend.seek(1.0)
    rgb = backend.read_frame()
    rgb_bytes = (rgb * 255).round_().byte().cpu()
    img = PIL.Image.fromarray(rgb_bytes.permute(1, 2, 0).numpy(), 'RGB')
    np.testing.assert_allclose(img, mid_frame_image, rtol=0, atol=50)


def test_pyav_duration(video_filename):
    backend = PyAvBackendFactory().create(video_filename, 'cpu')
    assert backend.duration == 2.0


def test_pyav_frame_rate(video_filename):
    backend = PyAvBackendFactory().create(video_filename, 'cpu')
    assert backend.frame_rate == 25
