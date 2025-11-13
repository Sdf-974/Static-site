import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Bom, dià!")
        self.assertEqual(node.to_html(), "<a>Bom, dià!</a>")
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bonne journée!")
        self.assertEqual(node.to_html(), "<b>Bonne journée!</b>")
    def test_leaf_to_html_wprops(self):
        node = LeafNode("b", "Hello, world!", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<b href="https://boot.dev">Hello, world!</b>')

if __name__ == "__main__":
    unittest.main()
