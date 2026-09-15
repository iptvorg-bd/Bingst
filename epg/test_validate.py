import importlib.util
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

spec = importlib.util.spec_from_file_location('validator', Path(__file__).with_name('validate.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class GuideValidation(unittest.TestCase):
    def guide(self, end, omit=False):
        ids = sorted(v.mappings()[1])
        channels = ''.join(f'<channel id="{i}"/>' for i in ids)
        start = (end - timedelta(hours=1)).strftime('%Y%m%d%H%M%S %z')
        stop = end.strftime('%Y%m%d%H%M%S %z')
        programmes = ''.join(f'<programme channel="{i}" start="{start}" stop="{stop}"><title>TEST ONLY</title></programme>' for i in (ids[:-1] if omit else ids))
        return f'<tv>{channels}{programmes}</tv>'

    def test_source_stays_disabled(self):
        with self.assertRaises(AssertionError):
            v.check_policy()

    def test_valid_guide_and_stale_or_partial_rejection(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'fixture.xml'
            future = datetime.now(timezone.utc) + timedelta(hours=2)
            path.write_text(self.guide(future))
            v.validate_guide(path)
            for content in (self.guide(future, omit=True), self.guide(future - timedelta(days=3)), '<html/>', '<tv/>'):
                path.write_text(content)
                with self.assertRaises(AssertionError):
                    v.validate_guide(path)


if __name__ == '__main__':
    unittest.main()
