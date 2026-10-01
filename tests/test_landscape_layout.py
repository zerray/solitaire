from pathlib import Path
import json
import subprocess
import unittest


class LandscapeLayoutTest(unittest.TestCase):
    def run_layout(self, viewport_width, viewport_height, board_top, bottom_inset):
        html = (Path(__file__).parents[1] / "index.html").read_text()
        script = html.split("<script>", 1)[1].split("// Boot", 1)[0]
        node_script = f"""
const vm = require('vm');
const source = {json.dumps(script)};
const noopElement = {{ addEventListener() {{}}, style: {{}} }};
const context = {{
  console: {{ log: console.log }},
  window: {{ addEventListener() {{}} }},
  document: {{ getElementById() {{ return noopElement; }} }},
  localStorage: {{ getItem() {{ return null; }} }},
  setInterval, clearInterval, setTimeout, clearTimeout,
  Math, Date, JSON
}};
vm.runInNewContext(source, context);
console.log(JSON.stringify(context.getBoardWidthForViewport(
  {viewport_width}, {viewport_height}, {board_top}, {bottom_inset}
)));
"""
        result = subprocess.run(
            ["node", "-e", node_script],
            check=True,
            capture_output=True,
            text=True,
        )
        return float(result.stdout.strip().splitlines()[-1])

    def test_landscape_width_fits_a_fixed_13_card_tableau(self):
        board_width = self.run_layout(844, 390, 58, 6)
        self.assertLessEqual(board_width, 844 * 0.96)

        board_height_per_card_width = (1 + 13 * 0.18) * 1.45
        expected_board_width = min(
            844 * 0.96,
            (390 - 58 - 6) / board_height_per_card_width * 12.4,
        )
        self.assertAlmostEqual(board_width, expected_board_width)

        card_width = board_width / 12.4
        board_height = board_height_per_card_width * card_width
        self.assertLessEqual(board_height, 390 - 58 - 6 + 1e-9)

    def test_portrait_layout_keeps_the_existing_width_limit(self):
        board_width = self.run_layout(390, 844, 100, 60)
        self.assertAlmostEqual(board_width, 390 * 0.94)


if __name__ == "__main__":
    unittest.main()
