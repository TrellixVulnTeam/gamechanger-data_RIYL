from collections import defaultdict

DISPLAY_TYPE_LOOKUP = defaultdict(lambda: "Document", {
    # This file should not be added too, use properties on the spider to assign these values
    "dod": 'Issuance',
    "dodm": 'Manual',
    "dodi": 'Instruction',
    "dodd": 'Directive',
    "cjcs": 'Notice',
    "cjcsi": 'Instruction',
    "cjcsm": 'Manual',
    "cjcsg": 'Guide',
    "icd": 'Directive',
    "icpg": 'Guide',
    "icpm": 'Manual',
    "title": 'Title',
    "dep": 'Memorandum',
    "sec": 'Memorandum',
    "ai": 'Instruction',
    "dtm": 'Memorandum',
    "eo": 'Order',
    "organization": 'Organization',
    "person": 'Person',
    "ombm": 'Memorandum',
    "opnavnote": 'Notice',
    "secnavnote": 'Notice',
    "opnavinst": 'Instruction',
    "secnavinst": 'Instruction',
    "comnavresforcominst": 'Instruction',
    "comnavresforcomnote": 'Notice',
    "navmed": 'Manual',
    "bumednote": 'Notice',
    "bumedinst": 'Instruction',
    "h.con.res.": 'Legislation',
    "h.j.res.": 'Legislation',
    "h.r.": 'Legislation',
    "h. res.": 'Legislation',
    "s.": 'Legislation',
    "s. con. res.": 'Legislation',
    "s.j. res.": 'Legislation',
    "s. res.": 'Legislation',
    "usar cir": 'Circular',
    "usar pam": 'Pamphlet',
    "usar reg": 'Regulation',
    "memo": "Memorandum",
    "dfar": "Regulation",
    "far": "Regulation",
    "cngbi": "Instruction",
    "cim": "Manual",
    "ci": "Instruction",
    "cn": "Notice",
    "ccn": "Notice",
    "dcmsi": "Instruction",
    "dod coronavirus guidance": "Guidance",
    # "cfr index": "CFR Index",
    # "cfr title": "CFR Title",
    # This file should not be added too, use properties on the spider to assign these values
})


CRAWLER_TO_DISPLAY_ORG_LOOKUP = defaultdict(lambda: "Uncategorized", {
    # This file should not be added too, use properties on the spider to assign these values
    "dod_issuances": "Dept. of Defense",
    "jcs_pubs": 'Joint Chiefs of Staff',
    "jcs_manual_uploads": 'Joint Chiefs of Staff',
    "dod_manual_uploads": 'Dept. of Defense',
    "army_manual_uploads": 'Dept. of the Army',
    "ic_policies": 'Intelligence Community',
    "us_code": 'United States Code',
    "ex_orders": 'Executive Branch',
    "opm_pubs": "OPM",
    "air_force_pubs": 'Dept. of the Air Force',
    "army_pubs": 'Dept. of the Army',
    "marine_pubs": 'US Marine Corps',
    "secnav_pubs": 'US Navy',
    "navy_reserves": 'US Navy Reserve',
    "navy_med_pubs": 'US Navy Medicine',
    "Bupers_Crawler": 'US Navy',
    "milpersman_crawler": "US Navy",
    "nato_stanag": "NATO",
    "fmr_pubs": "FMR",
    "legislation_pubs": "Congress",
    "Army_Reserve": "Dept. of the Army",
    "Memo": "Dept. of Defense",
    "dha_pubs": "Defense Health Agency",
    "jumbo_DFAR": "DFARS",
    "jumbo_FAR": "FAR",
    "National_Guard": "National Guard",
    "Coast_Guard": "Coast Guard",
    "jumbo_DFARS": "DFARS",
    "DOD_Coronavirus_Guidance": "Dept. of Defense",
    "dfar_subpart_regs": "DFARS",
    "far_subpart_regs": "FAR",
    # "code_of_federal_regulations": "Congress",
    # This file should not be added too, use properties on the spider to assign these values
})

CRAWLER_TO_DATA_SOURCE_LOOKUP = defaultdict(lambda: "Unlisted Source", {
    # This file should not be added too, use properties on the spider to assign these values
    "dod_issuances": "WHS DoD Directives Division",
    "army_pubs": "Army Publishing Directorate",
    "jcs_pubs": "CJCS Directives Library",
    "jcs_manual_uploads": "Joint Chiefs of Staff",
    "dod_manual_uploads": "Dept. of Defense",
    "army_manual_uploads": "Dept. of the Army",
    "ic_policies": "Office of Director of National Intelligence",
    "us_code": "Office of the Law Revision Counsel",
    "ex_orders": "Federal Register",
    "opm_pubs": "Executive Office of the President",
    "air_force_pubs": "Dept. of the Air Force E-Publishing",
    "marine_pubs": "Marine Corps Publications Electronic Library",
    "secnav_pubs": "Dept. of the Navy Issuances",
    "navy_reserves": "U.S. Navy Reserve",
    "navy_med_pubs": "Navy Medicine",
    "Bupers_Crawler": "MyNavy HR",
    "milpersman_crawler": "MyNavy HR",
    "nato_stanag": "NATO Publications",
    "fmr_pubs": "Under Secretary of Defense (Comptroller)",
    "legislation_pubs": "U.S. Government Publishing Office",
    "Army_Reserve": "Army Publishing Directorate",
    "Memo": "OSD Executive Secretary",
    "dha_pubs": "Military Health System",
    "jumbo_FAR": "Acquisition Publications",
    "jumbo_DFAR": "Acquisition Publications",
    "jumbo_far_dfar_crawler": "Acquisition Regulation",
    "National_Guard": "National Guard Bureau Publications & Forms Library",
    "Coast_Guard": "Coast Guard Deputy Commandant for Mission Support",
    "DOD_Coronavirus_Guidance": "Defense Publications",
    "dfar_subpart_regs": "Acquisition Publications",
    "far_subpart_regs": "Acquisition Publications",
    "code_of_federal_regulations": "U.S. Government Publishing Office",
    # This file should not be added too, use properties on the spider to assign these values
})

CRAWLER_TO_SOURCE_TITLE_LOOKUP = defaultdict(lambda: "Unlisted Source", {
    # This file should not be added too, use properties on the spider to assign these values
    "dod_issuances": "WHS DoD Directives",
    "army_pubs": "U.S Army Publications",
    "jcs_pubs": "Joint Chiefs of Staff Publications",
    "jcs_manual_uploads": "Joint Chiefs of Staff Additional Publications",
    "dod_manual_uploads": "Dept. of Defense Publications",
    "army_manual_uploads": "Dept. of the Army Publications",
    "ic_policies": "Intelligence Community Publications",
    "us_code": "United States Code",
    "ex_orders": "Executive Orders",
    "opm_pubs": "Office of Budget and Management Memoranda",
    "air_force_pubs": "Air Force Publications",
    "marine_pubs": "Marine Corps Orders",
    "secnav_pubs": "Dept. of the Navy Issuances",
    "navy_reserves": "U.S. Navy Reserve Publications",
    "navy_med_pubs": "Navy Medicine Directives",
    "Bupers_Crawler": "Bureau of Naval Personnel Instructions",
    "milpersman_crawler": "MILPERSMAN",
    "nato_stanag": "NATO Publications",
    "fmr_pubs": "DoD Financial Management Regulation",
    "legislation_pubs": "Congressional Legislation",
    "Army_Reserve": "U.S. Army Reserve Publications",
    "Memo": "Memorandums",
    "dha_pubs": "Defense Health Agency Publications",
    "jumbo_FAR": "Federal Acquisition Regulation",
    "jumbo_DFAR": "Defense Federal Acquisition Regulation Supplement",
    "jumbo_far_dfar_crawler": "Federal Acquisition Regulation",
    "National_Guard": "Chief National Guard Bureau Publications",
    "Coast_Guard": "Coast Guard Directives",
    "DOD_Coronavirus_Guidance": "DoD Coronavirus Guidance",
    "dfar_subpart_regs": "Defense Federal Acquisition Regulation Supplement",
    "far_subpart_regs": "Federal Acquisition Regulation",
    "code_of_federal_regulations": "Code of Federal Regulations",
    # This file should not be added too, use properties on the spider to assign these values
})