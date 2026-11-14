"""記譜体系・調律写像・表示規約を分離し、リズムと時間構造も正確な値で扱う音楽理論ライブラリ.

具体的な体系は ``aulos.western.equal``、``aulos.western.just``、``aulos.pentatonic`` にあり、
音高・和音・音階は名前の文字列から生成する。リズムと時間構造は ``aulos.rhythm`` が公開する。
新しい体系を定義するための部品は ``aulos.base`` にある。
"""

__all__ = []
