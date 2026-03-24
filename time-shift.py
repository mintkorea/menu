def render_unified_table(df, highlight_idx=None):
    # 헤더와 데이터가 어긋나지 않도록 하나의 HTML 태그로 묶음
    html = f"""
    <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; font-size: 11px; table-layout: fixed;">
            <thead>
                <tr style="background-color: #f8f9fa;">
                    <th style="border: 1px solid #ddd; width: 22%;">시간</th>
                    <th style="border: 1px solid #ddd; width: 19.5%; background:#FFF2CC;">성희</th>
                    <th style="border: 1px solid #ddd; width: 19.5%; background:#FFF2CC;">{seonghui}</th>
                    <th style="border: 1px solid #ddd; width: 19.5%; background:#D9EAD3;">의산A</th>
                    <th style="border: 1px solid #ddd; width: 19.5%; background:#D9EAD3;">의산B</th>
                </tr>
            </thead>
            <tbody>
    """
    for i, row in df.iterrows():
        bg = "background-color: #FFE5E5; font-weight: bold;" if i == highlight_idx else ""
        html += f"""
                <tr style="{bg}">
                    <td style="border: 1px solid #ddd; padding: 5px 2px; text-align: center; white-space: nowrap;">{row['From']}~{row['To']}</td>
                    <td style="border: 1px solid #ddd; padding: 5px 2px; text-align: center;">{row[jojang]}</td>
                    <td style="border: 1px solid #ddd; padding: 5px 2px; text-align: center;">{row[seonghui]}</td>
                    <td style="border: 1px solid #ddd; padding: 5px 2px; text-align: center;">{row[uisanA]}</td>
                    <td style="border: 1px solid #ddd; padding: 5px 2px; text-align: center;">{row[uisanB]}</td>
                </tr>
        """
    html += "</tbody></table></div>"
    return html

