"""Citation, license, and codebase information tab for the MP Methods Navigator."""

from __future__ import annotations

import streamlit as st

PAPER_TITLE = (
    "Learning from history instead of reinventing the wheel: "
    "A call for coordinating microplastics research, reporting, "
    "and publication criteria across disciplines"
)

AUTHORS = [
    {
        "name": "Granek, Elise F.",
        "affiliation": "Environmental Science & Management, Portland State University, Oregon, USA",
    },
    {
        "name": "Brander, Susanne M.",
        "affiliation": (
            "Oregon State University, College of Agricultural Sciences, "
            "Corvallis, Oregon, 97331, USA"
        ),
    },
    {
        "name": "Coffin, Scott",
        "affiliation": (
            "Office of Environmental Health Hazard Assessment, "
            "1001 I. St., Sacramento, California, 95814, United States of America"
        ),
    },
    {
        "name": "El Hayek, Eliane",
        "affiliation": (
            "Department of Pharmaceutical Sciences, University of New Mexico, "
            "College of Pharmacy, MSC09 5360, Albuquerque, New Mexico 87131, USA"
        ),
    },
    {
        "name": "Thornton Hampton, Leah M.",
        "affiliation": (
            "Toxicology Department, Southern California Coastal Water Research Project, "
            "3535 Harbor Blvd. Suite 110, Costa Mesa, CA, 92626-1437, USA"
        ),
    },
    {
        "name": "Seeley, Meredith Evans",
        "affiliation": (
            "Virginia Institute of Marine Science, William & Mary, "
            "Gloucester Point, VA 23062, USA"
        ),
    },
    {
        "name": "Gray, Andrew B.",
        "affiliation": (
            "Department of Environmental Sciences, University of California, Riverside, "
            "Riverside, California, 92521, USA"
        ),
    },
    {
        "name": "Harper, Stacey L.",
        "affiliation": (
            "Oregon State University, College of Agricultural Sciences / College of Engineering, "
            "Corvallis, Oregon, 97331, USA"
        ),
    },
]

GITHUB_URL = "https://github.com/ScottCoffin/Quality-Manuscript"

GITHUB_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
     fill="currentColor" style="vertical-align:middle; margin-right:6px;">
  <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577
           v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756
           -1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237
           1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604
           -2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221
           -.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23
           A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404
           2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176
           .77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921
           .43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576
           C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
</svg>"""

AGPL_TEXT = """\
This tool is released under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

The AGPL-3.0 is a copyleft license that requires anyone who runs a modified version of this
software over a network to make the complete corresponding source code available.

Key conditions:
- **Use** — Free to use for any purpose.
- **Distribute** — May distribute copies of the original or modified software.
- **Modify** — May modify the source code, but modifications must also be released under AGPL-3.0.
- **Network use** — If you deploy a modified version as a web service, you must provide the
  source code to users of that service.
- **Attribution** — The original copyright notice and license must be preserved.

Full license text: https://www.gnu.org/licenses/agpl-3.0.html
"""


def render_citation_tab():
    """Render the citation, codebase, and license tab."""

    # ── Paper citation ───────────────────────────────────────────────────────
    st.markdown("### Companion Publication")
    st.markdown(
        f"This tool accompanies the following manuscript *(submitted / in review)*:"
    )

    st.info(f"**{PAPER_TITLE}**", icon="📄")

    # Author list
    st.markdown("#### Authors")
    for i, author in enumerate(AUTHORS, start=1):
        st.markdown(
            f"<div style='margin-bottom:4px;'>"
            f"<strong>{i}. {author['name']}</strong>"
            f"<br/><span style='color:#555; font-size:0.88em;'>{author['affiliation']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Formatted draft citation block
    st.markdown("#### Suggested Citation *(draft — update with journal/DOI when published)*")
    author_short = (
        "Granek, E.F., Brander, S.M., Coffin, S., El Hayek, E., "
        "Thornton Hampton, L.M., Seeley, M.E., Gray, A.B., & Harper, S.L."
    )
    citation_text = (
        f"{author_short} (in review). {PAPER_TITLE}. "
        f"[Journal TBD]. DOI: TBD"
    )
    st.code(citation_text, language=None)

    st.divider()

    # ── Codebase ─────────────────────────────────────────────────────────────
    st.markdown("### Codebase")
    st.markdown(
        f"{GITHUB_LOGO_SVG}"
        f"<a href='{GITHUB_URL}' target='_blank' style='font-size:1.05em; font-weight:600;'>"
        f"ScottCoffin/Quality-Manuscript</a>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"The source code for this tool — including the decision tree configuration, "
        f"crosswalk data, and Streamlit application — is publicly available at:"
    )
    st.markdown(
        f"<a href='{GITHUB_URL}' target='_blank'>{GITHUB_URL}</a>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── License ──────────────────────────────────────────────────────────────
    st.markdown("### License")
    st.markdown(AGPL_TEXT)

    st.markdown(
        "<div style='font-size:0.82em; color:#888; margin-top:8px;'>"
        "Copyright © 2026 the authors listed above. "
        "Crosswalk data and decision tree content are released under the same license."
        "</div>",
        unsafe_allow_html=True,
    )
