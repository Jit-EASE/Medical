"""
╔══════════════════════════════════════════════════════════════════════╗
║  EU MEDICAL ACTS EXPLORER                                          ║
║  Powered by EUR-Lex CELLAR SPARQL API                              ║
║  © 2026 Shubhojit Bagchi — PhD Research, Ireland                   ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import requests
import json
import html as html_mod
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SPARQL_ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql"

def celex_url(celex):
    return f"https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:{celex}"

def summary_url(celex):
    return f"https://eur-lex.europa.eu/legal-content/EN/LSU/?uri=CELEX:{celex}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CURATED MEDICAL ACTS DATABASE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEDICAL_ACTS = [
    {
        "name": "Medical Devices Regulation (MDR)",
        "celex": "32017R0745",
        "year": 2017,
        "type": "Regulation",
        "category": "Medical Devices",
        "in_force": True,
        "summary": (
            "The Medical Devices Regulation (EU) 2017/745 is the cornerstone of EU medical device law. "
            "It replaced the earlier Medical Devices Directive (93/42/EEC) and the Active Implantable "
            "Medical Devices Directive (90/385/EEC). The regulation governs the entire lifecycle of "
            "medical devices — from design and manufacturing through clinical evaluation, market "
            "placement, and post-market surveillance. It introduced stricter requirements for clinical "
            "evidence, tighter controls on notified bodies, and a new risk classification system."
        ),
        "what_it_means": (
            "If you manufacture, distribute, or use medical devices in the EU, this regulation defines "
            "what you must do. Devices are classified into risk classes (I, IIa, IIb, III), and the "
            "higher the risk, the more evidence and oversight is required before the device can be sold. "
            "The regulation also created the EUDAMED database for tracking devices and the Unique Device "
            "Identification (UDI) system so every device can be traced."
        ),
        "key_provisions": [
            "Risk-based classification: Class I (low risk) through Class III (highest risk, e.g. implants)",
            "Clinical evidence: Manufacturers must demonstrate safety and performance through clinical data",
            "Unique Device Identification (UDI): Every device gets a traceable identifier",
            "EUDAMED: Centralised European database for device registration and vigilance",
            "Notified bodies: Stricter designation and oversight of bodies that certify devices",
            "Post-market surveillance: Ongoing obligation to monitor devices after they reach the market",
            "Economic operators: Clear responsibilities for manufacturers, importers, and distributors",
            "Implant cards: Patients with implants receive identification cards with device information",
        ],
        "who_it_affects": "Medical device manufacturers, notified bodies, importers, distributors, healthcare providers, patients with implanted devices",
    },
    {
        "name": "In Vitro Diagnostic Regulation (IVDR)",
        "celex": "32017R0746",
        "year": 2017,
        "type": "Regulation",
        "category": "Medical Devices",
        "in_force": True,
        "summary": (
            "Regulation (EU) 2017/746 governs in vitro diagnostic medical devices — the tests, reagents, "
            "and instruments used to examine specimens derived from the human body (blood tests, genetic "
            "tests, COVID tests, pregnancy tests, etc.). It replaced Directive 98/79/EC with a much more "
            "rigorous framework, introducing risk-based classification and mandatory third-party assessment "
            "for higher-risk diagnostics."
        ),
        "what_it_means": (
            "Previously, most IVDs were self-certified by manufacturers. Under the IVDR, around 80% of "
            "IVDs now require assessment by a notified body. This is a massive shift. The regulation "
            "ensures that diagnostic tests — which directly influence treatment decisions — meet high "
            "standards of accuracy and reliability."
        ),
        "key_provisions": [
            "New risk classification: Classes A (lowest) through D (highest, e.g. blood screening for HIV)",
            "Notified body involvement required for Classes B, C, and D devices",
            "Performance evaluation: Manufacturers must prove analytical and clinical performance",
            "Companion diagnostics: Tests used to select patients for specific treatments are regulated",
            "EU Reference Laboratories: Established to verify performance of high-risk IVDs",
            "Post-market performance follow-up: Continuous monitoring of diagnostic accuracy",
        ],
        "who_it_affects": "IVD manufacturers, laboratories, notified bodies, clinicians relying on diagnostic results, patients",
    },
    {
        "name": "Clinical Trials Regulation",
        "celex": "32014R0536",
        "year": 2014,
        "type": "Regulation",
        "category": "Clinical Trials",
        "in_force": True,
        "summary": (
            "Regulation (EU) No 536/2014 harmonises the rules for conducting clinical trials of medicinal "
            "products across all EU Member States. It replaced the earlier Clinical Trials Directive "
            "(2001/20/EC) which had led to fragmented implementation. The regulation introduced the "
            "Clinical Trials Information System (CTIS) — a single portal for submitting, authorising, "
            "and supervising clinical trials across the EU."
        ),
        "what_it_means": (
            "Before this regulation, a company running a clinical trial in multiple EU countries had to "
            "submit separate applications to each country. Now there is one application through CTIS, "
            "with coordinated assessment. This makes it faster and cheaper to run multi-country trials "
            "while maintaining safety oversight. It also increases transparency — trial information is "
            "publicly accessible in the database."
        ),
        "key_provisions": [
            "Single submission portal (CTIS): One application for trials across multiple Member States",
            "Coordinated assessment: One reporting Member State leads, others collaborate",
            "Strict timelines: Authorities must respond within defined periods",
            "Low-intervention trials: Simplified rules for trials using already-authorised medicines",
            "Transparency: Public access to trial protocols, results, and summaries",
            "Safety reporting: Harmonised rules for reporting suspected unexpected serious adverse reactions",
            "Informed consent: Strengthened requirements for participant information and consent",
        ],
        "who_it_affects": "Pharmaceutical companies, clinical research organisations, investigators, ethics committees, trial participants",
    },
    {
        "name": "Directive on Medicinal Products for Human Use",
        "celex": "32001L0083",
        "year": 2001,
        "type": "Directive",
        "category": "Pharmaceuticals",
        "in_force": True,
        "summary": (
            "Directive 2001/83/EC is the foundational EU Community Code for medicinal products. It "
            "establishes the complete regulatory framework for the authorisation, manufacture, labelling, "
            "distribution, advertising, and pharmacovigilance of medicines for human use. Almost every "
            "medicine sold in the EU is governed by this directive or the centralised regulation that "
            "complements it."
        ),
        "what_it_means": (
            "This is the 'constitution' of EU pharmaceutical law. It says that no medicine can be placed "
            "on the market without a marketing authorisation, which requires proof of quality, safety, "
            "and efficacy. It also sets rules for generics, biosimilars, homeopathic products, and "
            "traditional herbal medicines. If you work in pharma in the EU, this directive underpins "
            "almost everything you do."
        ),
        "key_provisions": [
            "Marketing authorisation: Required before any medicine can be sold — must prove quality, safety, efficacy",
            "Manufacturing authorisation: Producers must hold a licence and follow Good Manufacturing Practice (GMP)",
            "Labelling and package leaflets: Standardised information requirements for all medicines",
            "Pharmacovigilance: Obligation to monitor and report adverse drug reactions",
            "Generics and biosimilars: Simplified authorisation pathways referencing originator data",
            "Prescription vs non-prescription: Classification rules for medicinal products",
            "Advertising: Strict rules on promotion to healthcare professionals and the public",
            "Wholesale distribution: Requirements for distributors including GDP compliance",
        ],
        "who_it_affects": "Pharmaceutical companies, generic manufacturers, wholesalers, pharmacies, prescribers, patients",
    },
    {
        "name": "Centralised Marketing Authorisation Regulation",
        "celex": "32004R0726",
        "year": 2004,
        "type": "Regulation",
        "category": "Pharmaceuticals",
        "in_force": True,
        "summary": (
            "Regulation (EC) No 726/2004 establishes the centralised procedure for authorising medicines "
            "via the European Medicines Agency (EMA). Under this route, a single application to EMA leads "
            "to a marketing authorisation valid in all EU Member States simultaneously. It is mandatory "
            "for certain categories of medicines including biotechnology products, orphan medicines, and "
            "medicines for HIV, cancer, diabetes, and neurodegenerative diseases."
        ),
        "what_it_means": (
            "Instead of applying to each country separately, companies can get one EU-wide authorisation "
            "through EMA. This is the route used for the most innovative and high-impact medicines. EMA's "
            "scientific committee (CHMP) evaluates the application and the European Commission grants the "
            "authorisation. Once approved, the medicine can be marketed across the entire EU and EEA."
        ),
        "key_provisions": [
            "Centralised procedure: Single application leading to EU-wide marketing authorisation",
            "Mandatory scope: Required for biotech products, orphan drugs, advanced therapies, and certain disease areas",
            "EMA scientific assessment: Committee for Medicinal Products for Human Use (CHMP) evaluates",
            "European Commission decision: Final authorisation granted at EU level",
            "Post-authorisation obligations: Ongoing safety monitoring, periodic safety update reports",
            "Conditional marketing authorisation: For unmet medical needs with less complete data",
            "Pharmacovigilance: Centralised safety signal detection and risk management",
        ],
        "who_it_affects": "Innovative pharmaceutical and biotech companies, EMA, national medicines agencies, healthcare systems",
    },
    {
        "name": "Falsified Medicines Directive",
        "celex": "32011L0062",
        "year": 2011,
        "type": "Directive",
        "category": "Pharmaceuticals",
        "in_force": True,
        "summary": (
            "Directive 2011/62/EU amends the Community Code to address the growing threat of falsified "
            "medicines entering the legal supply chain. It introduced mandatory safety features on "
            "medicine packaging — including a unique identifier (serialisation) and an anti-tampering "
            "device — and created a framework for verifying medicines at the point of dispensing."
        ),
        "what_it_means": (
            "Every prescription medicine pack in the EU now carries a 2D barcode that pharmacies scan "
            "before dispensing. If the code does not match the European verification system, the medicine "
            "is flagged as potentially falsified. The directive also regulates online pharmacies, requiring "
            "them to display a common EU logo that patients can click to verify legitimacy."
        ),
        "key_provisions": [
            "Unique identifier: 2D data matrix code on every prescription medicine pack",
            "Anti-tampering device: Evidence of package opening visible to patients and pharmacists",
            "End-to-end verification: Medicines verified at manufacturing, wholesale, and dispensing stages",
            "Common EU logo: Mandatory logo for legitimate online pharmacies, linked to national registers",
            "Active substance registration: Importers and manufacturers of active pharmaceutical ingredients must register",
            "Broker registration: Intermediaries who negotiate medicine sales must be registered",
        ],
        "who_it_affects": "Pharmacies, pharmaceutical manufacturers, wholesale distributors, online pharmacies, patients",
    },
    {
        "name": "Orphan Medicinal Products Regulation",
        "celex": "32000R0141",
        "year": 2000,
        "type": "Regulation",
        "category": "Pharmaceuticals",
        "in_force": True,
        "summary": (
            "Regulation (EC) No 141/2000 provides a framework of incentives for developing medicines for "
            "rare diseases (affecting fewer than 5 in 10,000 people in the EU). Without incentives, the "
            "small patient populations make these medicines commercially unviable. The regulation created "
            "the orphan designation process and offers significant rewards to encourage development."
        ),
        "what_it_means": (
            "Rare disease patients often had no treatment options because the market was too small for "
            "pharma companies to invest. This regulation changed that by offering 10 years of market "
            "exclusivity — meaning no similar medicine can be authorised for the same condition during "
            "that period. Combined with fee reductions and protocol assistance from EMA, it has led to "
            "hundreds of orphan medicines reaching patients."
        ),
        "key_provisions": [
            "Orphan designation: Granted by EMA's Committee for Orphan Medicinal Products (COMP)",
            "10-year market exclusivity: No similar product authorised for the same indication",
            "Protocol assistance: Scientific advice from EMA at reduced fees",
            "Fee reductions: Lower regulatory fees for orphan medicine applications",
            "EU funding access: Eligibility for EU research and development programmes",
            "Designation criteria: Disease must affect < 5 in 10,000 EU population, or be commercially unviable without incentives",
        ],
        "who_it_affects": "Rare disease patients and families, biotech/pharma companies, EMA, patient advocacy groups, healthcare payers",
    },
    {
        "name": "Paediatric Regulation",
        "celex": "32006R1901",
        "year": 2006,
        "type": "Regulation",
        "category": "Pharmaceuticals",
        "in_force": True,
        "summary": (
            "Regulation (EC) No 1901/2006 addresses the lack of medicines specifically tested and "
            "authorised for use in children. It requires companies developing new medicines to submit a "
            "Paediatric Investigation Plan (PIP) to EMA's Paediatric Committee (PDCO), ensuring that "
            "paediatric studies are conducted unless a waiver or deferral is granted."
        ),
        "what_it_means": (
            "Before this regulation, most medicines given to children had never been formally tested in "
            "children — dosing was often guesswork. The PIP requirement means that when companies develop "
            "new medicines, they must also plan studies in children. In return, they receive a 6-month "
            "extension of their Supplementary Protection Certificate (SPC), which extends their patent-like "
            "exclusivity."
        ),
        "key_provisions": [
            "Paediatric Investigation Plans (PIPs): Mandatory development plan for paediatric studies",
            "Paediatric Committee (PDCO): EMA committee that assesses and agrees PIPs",
            "Waivers and deferrals: Exemptions if a medicine is unsuitable or unsafe for children",
            "6-month SPC extension: Reward for completing paediatric studies",
            "Paediatric-use marketing authorisation (PUMA): Dedicated authorisation for paediatric-only medicines",
            "Paediatric formulations: Encouragement to develop age-appropriate dosage forms",
        ],
        "who_it_affects": "Children and their families, paediatricians, pharmaceutical companies, EMA/PDCO, clinical researchers",
    },
    {
        "name": "Advanced Therapy Medicinal Products (ATMP) Regulation",
        "celex": "32007R1394",
        "year": 2007,
        "type": "Regulation",
        "category": "Pharmaceuticals",
        "in_force": True,
        "summary": (
            "Regulation (EC) No 1394/2007 creates specific rules for advanced therapy medicinal products "
            "— a category covering gene therapy, somatic cell therapy, and tissue-engineered products. "
            "These are cutting-edge treatments that modify genes, use living cells as medicines, or "
            "engineer tissues for transplantation."
        ),
        "what_it_means": (
            "Gene therapies like those for spinal muscular atrophy, CAR-T cell treatments for cancer, "
            "and tissue-engineered skin grafts all fall under this regulation. Because these products "
            "blur the line between medicines and medical procedures, specific rules were needed. The "
            "Committee for Advanced Therapies (CAT) at EMA provides expert assessment. A hospital "
            "exemption allows non-industrial ATMPs to be used under national rules."
        ),
        "key_provisions": [
            "Centralised authorisation: All ATMPs must go through EMA for EU-wide approval",
            "Committee for Advanced Therapies (CAT): Specialist EMA committee for ATMP assessment",
            "Risk-based approach: Requirements proportionate to novelty and complexity",
            "Traceability: 30-year requirement to trace patients who receive ATMPs",
            "Post-authorisation follow-up: Long-term efficacy and safety monitoring",
            "Hospital exemption: Non-routine use of non-industrial ATMPs under national oversight",
            "Combined ATMPs: Rules for products incorporating medical devices (e.g. cell-seeded scaffolds)",
        ],
        "who_it_affects": "Gene therapy developers, cell therapy manufacturers, tissue engineering companies, hospitals, oncologists, rare disease specialists",
    },
    {
        "name": "Health Technology Assessment (HTA) Regulation",
        "celex": "32021R2282",
        "year": 2021,
        "type": "Regulation",
        "category": "Health Technology",
        "in_force": True,
        "summary": (
            "Regulation (EU) 2021/2282 establishes a framework for joint clinical assessments of health "
            "technologies at EU level. Previously, each Member State conducted its own assessment, leading "
            "to duplication and delays. The regulation creates EU-level joint work on clinical assessments "
            "of new medicines and medical devices."
        ),
        "what_it_means": (
            "When a new cancer drug or innovative medical device reaches the market, each country used to "
            "independently assess whether it works better than existing treatments. Now, a single joint "
            "clinical assessment is performed at EU level through a Coordination Group. National bodies "
            "can then focus on local context — pricing, budget impact, and ethical considerations. "
            "Implementation is phased: oncology and ATMPs first (from 2025), then all medicines by 2030."
        ),
        "key_provisions": [
            "Joint clinical assessments: EU-level evaluation of clinical benefit for new health technologies",
            "Coordination Group on HTA: Member State body overseeing joint work",
            "Phased implementation: Oncology and ATMPs from Jan 2025, orphan drugs from 2028, all medicines by 2030",
            "Joint scientific consultations: Early dialogue between developers and HTA bodies",
            "Identification of emerging technologies: Horizon-scanning for future assessments",
            "National decision-making preserved: Pricing and reimbursement remain with Member States",
        ],
        "who_it_affects": "National HTA bodies, pharmaceutical companies, medical device manufacturers, healthcare payers, patients awaiting access to new treatments",
    },
    {
        "name": "Cross-Border Healthcare Directive",
        "celex": "32011L0024",
        "year": 2011,
        "type": "Directive",
        "category": "Patient Rights",
        "in_force": True,
        "summary": (
            "Directive 2011/24/EU on patients' rights in cross-border healthcare establishes the "
            "conditions under which a patient may travel to another EU Member State for medical "
            "treatment and be reimbursed by their home country. It also promotes cooperation on "
            "healthcare between Member States."
        ),
        "what_it_means": (
            "If you live in one EU country but want to receive treatment in another — perhaps because "
            "of shorter waiting times or specialist expertise — this directive gives you the right to "
            "do so and be reimbursed up to the amount your home country would have paid. For hospital "
            "care, prior authorisation may be required. Each country has a National Contact Point that "
            "provides information about available treatments and costs."
        ),
        "key_provisions": [
            "Right to cross-border healthcare: Patients can seek treatment in any EU Member State",
            "Reimbursement: Home country reimburses up to the amount it would have paid domestically",
            "Prior authorisation: May be required for hospital care or specialised treatments",
            "National Contact Points: Information offices in each Member State for patients",
            "eHealth Network: Voluntary cooperation on digital health and interoperability",
            "European Reference Networks (ERNs): Virtual networks for rare and complex diseases",
            "Mutual recognition of prescriptions: Prescriptions from one Member State recognised in others",
        ],
        "who_it_affects": "Patients seeking treatment abroad, healthcare providers, national health systems, rare disease patients",
    },
    {
        "name": "European Health Data Space (EHDS) Proposal",
        "celex": "52022PC0197",
        "year": 2022,
        "type": "Proposal",
        "category": "Health Data",
        "in_force": False,
        "summary": (
            "The proposed EHDS regulation aims to create a common framework for the use of health data "
            "across the EU. It covers both primary use (patients accessing and controlling their own "
            "health records) and secondary use (researchers, regulators, and policymakers accessing "
            "anonymised health data for public interest purposes)."
        ),
        "what_it_means": (
            "Imagine being able to access your medical records from any hospital in any EU country "
            "through a standardised digital system. That is the primary use vision. For secondary use, "
            "researchers could access large pools of anonymised health data across borders to study "
            "disease patterns, evaluate treatments, or train AI models — all governed by strict access "
            "rules through Health Data Access Bodies in each Member State."
        ),
        "key_provisions": [
            "MyHealth@EU: Infrastructure for cross-border exchange of patient summaries, prescriptions, lab results",
            "Patient access rights: Citizens can access, download, and share their electronic health data",
            "Interoperability: Mandatory standards for electronic health record systems",
            "Secondary use framework: Controlled access to health data for research, policy, and innovation",
            "Health Data Access Bodies: National authorities managing secondary use applications",
            "Prohibited uses: Health data cannot be used for insurance discrimination or advertising",
        ],
        "who_it_affects": "Every EU citizen, hospitals and clinics, EHR system vendors, health researchers, AI developers, public health authorities",
    },
    {
        "name": "Substances of Human Origin (SoHO) Regulation",
        "celex": "32024R1610",
        "year": 2024,
        "type": "Regulation",
        "category": "Blood & Tissues",
        "in_force": True,
        "summary": (
            "Regulation (EU) 2024/1610 modernises and consolidates the EU rules for blood, tissues, "
            "cells, and other substances of human origin. It replaces the previous Blood Safety Directive "
            "(2002/98/EC) and Tissues and Cells Directive (2004/23/EC) with a single, technology-neutral "
            "framework."
        ),
        "what_it_means": (
            "The old directives were written when technologies like gene-modified cells, microbiome "
            "therapies, and 3D-printed tissues did not exist. This regulation creates a flexible "
            "framework that can accommodate new SoHO therapies without needing constant legislative "
            "updates. It introduces an EU SoHO Platform for oversight and strengthens both donor "
            "protection and recipient safety."
        ),
        "key_provisions": [
            "Single framework: Covers blood, tissues, cells, breast milk, faecal microbiota, and other SoHO",
            "Risk-based authorisation: SoHO activities assessed based on actual risk",
            "Technology-neutral: Designed to accommodate emerging therapies without legislative changes",
            "EU SoHO Platform: Digital system for registration, authorisation, and vigilance",
            "Donor protection: Enhanced standards for donor health assessment and informed consent",
            "Supply monitoring: Tools to prevent shortages of critical SoHO (e.g. blood supply)",
            "Traceability: From donor to recipient and back, for 30+ years",
        ],
        "who_it_affects": "Blood banks, tissue establishments, hospitals, transplant coordinators, donors, recipients, researchers using human-origin materials",
    },
    {
        "name": "Tissues and Cells Directive",
        "celex": "32004L0023",
        "year": 2004,
        "type": "Directive",
        "category": "Blood & Tissues",
        "in_force": True,
        "summary": (
            "Directive 2004/23/EC set the original EU quality and safety standards for the donation, "
            "procurement, testing, processing, preservation, storage, and distribution of human tissues "
            "and cells — including tissues for transplantation, reproductive cells (for IVF), and "
            "haematopoietic stem cells."
        ),
        "what_it_means": (
            "This directive ensured that when you receive a tissue transplant or undergo IVF in the EU, "
            "the biological materials have been handled according to consistent quality and safety "
            "standards. Tissue establishments must be accredited, and every step from donation to use "
            "must be traceable."
        ),
        "key_provisions": [
            "Tissue establishment accreditation: Must be authorised by national competent authorities",
            "Donor eligibility: Testing and selection criteria to minimise disease transmission risk",
            "Traceability: Every tissue/cell traced from donor through processing to recipient",
            "Serious adverse event reporting: Mandatory notification of incidents",
            "Quality management systems: Documented procedures, trained personnel, validated processes",
            "Third-country imports: Controls on tissues and cells imported from outside the EU",
        ],
        "who_it_affects": "Tissue banks, IVF clinics, transplant surgeons, haematopoietic stem cell registries, organ donation organisations",
    },
    {
        "name": "Blood Safety Directive",
        "celex": "32002L0098",
        "year": 2002,
        "type": "Directive",
        "category": "Blood & Tissues",
        "in_force": True,
        "summary": (
            "Directive 2002/98/EC establishes standards of quality and safety for collecting, testing, "
            "processing, storing, and distributing human blood and blood components. It enshrines the "
            "principle of voluntary and unpaid donation."
        ),
        "what_it_means": (
            "Every blood transfusion in the EU relies on the safety framework established by this "
            "directive. Blood establishments must follow strict quality systems, donors are assessed for "
            "eligibility, every donation is tested for infectious diseases, and any adverse event must be "
            "reported."
        ),
        "key_provisions": [
            "Voluntary unpaid donation: Fundamental principle of EU blood policy",
            "Blood establishment authorisation: Must be designated and inspected by national authorities",
            "Donor eligibility: Criteria for donor health assessment and deferral",
            "Mandatory testing: Blood tested for HIV, hepatitis B, hepatitis C, and other infections",
            "Haemovigilance: System for reporting serious adverse reactions and events",
            "Traceability: Donation-to-transfusion tracking maintained for 30 years",
            "Quality management: GMP-equivalent systems for blood establishments",
        ],
        "who_it_affects": "Blood donation services, hospitals performing transfusions, blood donors, patients receiving transfusions, national blood authorities",
    },
]

CATEGORIES = sorted(set(a["category"] for a in MEDICAL_ACTS))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SPARQL ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_sparql(query, timeout=30):
    try:
        r = requests.post(SPARQL_ENDPOINT, data={"query": query},
                          headers={"Accept": "application/sparql-results+json",
                                   "Content-Type": "application/x-www-form-urlencoded"},
                          timeout=timeout)
        r.raise_for_status()
        data = r.json()
        return [{v: b[v]["value"] for v in data["head"]["vars"] if v in b}
                for b in data.get("results", {}).get("bindings", [])]
    except Exception:
        return []


def sparql_search_health(term="", res_type="any", limit=40):
    tf = ""
    if res_type == "regulation":
        tf = "FILTER(?type IN (<http://publications.europa.eu/resource/authority/resource-type/REG>,<http://publications.europa.eu/resource/authority/resource-type/REG_IMPL>,<http://publications.europa.eu/resource/authority/resource-type/REG_DEL>))"
    elif res_type == "directive":
        tf = "FILTER(?type IN (<http://publications.europa.eu/resource/authority/resource-type/DIR>,<http://publications.europa.eu/resource/authority/resource-type/DIR_IMPL>,<http://publications.europa.eu/resource/authority/resource-type/DIR_DEL>))"
    txf = f'FILTER(CONTAINS(LCASE(STR(?title)), LCASE("{term.replace(chr(34), "")}")))' if term else ""
    return run_sparql(f"""
    PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?celex ?title ?date ?force ?type WHERE {{
        ?work cdm:work_has_resource-type ?type . ?work cdm:resource_legal_id_celex ?celex .
        OPTIONAL {{ ?work cdm:work_has_expression ?e . ?e cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> . ?e cdm:expression_title ?title . }}
        OPTIONAL {{ ?work cdm:work_date_document ?date . }}
        OPTIONAL {{ ?work cdm:resource_legal_in-force ?force . }}
        ?work cdm:work_is_about_concept_eurovoc ?s .
        FILTER(?s IN (<http://eurovoc.europa.eu/3885>,<http://eurovoc.europa.eu/3730>,<http://eurovoc.europa.eu/192>,<http://eurovoc.europa.eu/4636>,<http://eurovoc.europa.eu/5765>,<http://eurovoc.europa.eu/5932>,<http://eurovoc.europa.eu/1919>,<http://eurovoc.europa.eu/1854>,<http://eurovoc.europa.eu/4584>,<http://eurovoc.europa.eu/3371>,<http://eurovoc.europa.eu/4587>))
        {tf} {txf}
        FILTER NOT EXISTS {{ ?work cdm:work_has_resource-type <http://publications.europa.eu/resource/authority/resource-type/CORRIGENDUM> }}
        FILTER NOT EXISTS {{ ?work cdm:do_not_index "true"^^xsd:boolean }}
    }} ORDER BY DESC(?date) LIMIT {limit}""")


def sparql_celex(celex):
    return run_sparql(f"""
    PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT DISTINCT ?title ?date ?force ?type ?author ?subj WHERE {{
        ?work cdm:resource_legal_id_celex "{celex}" . ?work cdm:work_has_resource-type ?type .
        OPTIONAL {{ ?work cdm:work_has_expression ?e . ?e cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> . ?e cdm:expression_title ?title . }}
        OPTIONAL {{ ?work cdm:work_date_document ?date . }}
        OPTIONAL {{ ?work cdm:resource_legal_in-force ?force . }}
        OPTIONAL {{ ?work cdm:work_created_by_agent ?ag . ?ag skos:prefLabel ?author . FILTER(LANG(?author)="en") }}
        OPTIONAL {{ ?work cdm:work_is_about_concept_eurovoc ?sv . ?sv skos:prefLabel ?subj . FILTER(LANG(?subj)="en") }}
    }} LIMIT 30""")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Source+Sans+3:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root{--bg:#080e1a;--sf:#0f1929;--sf2:#15233d;--bd:#1c3054;--gold:#FFCC00;--ac:#5a9fd4;--tx:#dce4f0;--mu:#7e92ad;}
.stApp{background:var(--bg);}
.banner{background:linear-gradient(135deg,#002266,#001133);border:1px solid rgba(255,204,0,.12);border-radius:14px;padding:2rem 1.8rem;margin-bottom:1.5rem;position:relative;overflow:hidden;}
.banner::after{content:'';position:absolute;top:-40%;right:-15%;width:350px;height:350px;background:radial-gradient(circle,rgba(255,204,0,.05)0%,transparent 70%);}
.banner .stars{color:var(--gold);font-size:.9rem;letter-spacing:3px;}
.banner h1{font-family:'Playfair Display',serif;color:#fff;font-size:2rem;margin:.4rem 0 .2rem;}
.banner .sub{font-family:'Source Sans 3',sans-serif;color:var(--gold);font-size:.8rem;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;}
.banner .desc{font-family:'Source Sans 3',sans-serif;color:rgba(255,255,255,.55);font-size:.85rem;line-height:1.6;margin-top:.5rem;}
.abox{background:linear-gradient(150deg,var(--sf),var(--sf2));border:1px solid var(--bd);border-radius:12px;padding:1.4rem;margin-bottom:.4rem;}
.abox:hover{border-color:var(--ac);}
.abox h3{font-family:'Playfair Display',serif;color:#fff;font-size:1.1rem;margin:.3rem 0 .4rem;line-height:1.4;}
.abox .meta{font-family:'IBM Plex Mono',monospace;color:var(--ac);font-size:.74rem;}
.abox p,.abox .ex{font-family:'Source Sans 3',sans-serif;color:var(--mu);font-size:.87rem;line-height:1.75;}
.abox .sl{font-family:'Source Sans 3',sans-serif;color:var(--gold);font-size:.74rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;margin:1.1rem 0 .4rem;padding-top:.7rem;border-top:1px solid rgba(255,204,0,.08);}
.abox .pv{font-family:'Source Sans 3',sans-serif;color:var(--tx);font-size:.85rem;line-height:1.6;padding:.35rem 0 .35rem 1rem;border-left:2px solid var(--ac);margin-bottom:.3rem;}
.abox .af{font-family:'Source Sans 3',sans-serif;color:var(--mu);font-size:.82rem;font-style:italic;margin-top:.6rem;}
.b{display:inline-block;padding:2px 9px;border-radius:5px;font-family:'Source Sans 3',sans-serif;font-size:.68rem;font-weight:600;letter-spacing:.4px;text-transform:uppercase;margin-right:4px;margin-bottom:4px;}
.br{background:rgba(59,130,246,.12);color:#60a5fa;border:1px solid rgba(59,130,246,.2);}
.bd{background:rgba(168,85,247,.12);color:#c084fc;border:1px solid rgba(168,85,247,.2);}
.bp{background:rgba(20,184,166,.12);color:#5eead4;border:1px solid rgba(20,184,166,.2);}
.bc{background:rgba(255,204,0,.08);color:var(--gold);border:1px solid rgba(255,204,0,.15);}
.by{background:rgba(34,197,94,.1);color:#4ade80;border:1px solid rgba(34,197,94,.2);}
.bn{background:rgba(239,68,68,.1);color:#f87171;border:1px solid rgba(239,68,68,.2);}
.ba{font-family:'IBM Plex Mono',monospace;background:rgba(34,197,94,.08);color:#4ade80;border:1px solid rgba(34,197,94,.18);font-size:.63rem;}
.ll{display:inline-block;margin-top:.6rem;padding:5px 12px;background:rgba(0,51,153,.2);border:1px solid rgba(90,159,212,.25);border-radius:7px;color:var(--ac);text-decoration:none;font-family:'Source Sans 3',sans-serif;font-size:.8rem;font-weight:500;}
.ll:hover{background:rgba(0,51,153,.35);color:#fff;}
.st{background:var(--sf);border:1px solid var(--bd);border-radius:10px;padding:1rem;text-align:center;}
.st .n{font-family:'Playfair Display',serif;color:var(--gold);font-size:1.7rem;}
.st .l{font-family:'Source Sans 3',sans-serif;color:var(--mu);font-size:.7rem;text-transform:uppercase;letter-spacing:.8px;margin-top:.15rem;}
.sc{background:var(--sf);border:1px solid var(--bd);border-radius:10px;padding:1.1rem;margin-bottom:.7rem;}
.sc:hover{border-color:var(--ac);}
.sc h4{font-family:'Playfair Display',serif;color:#fff;font-size:.95rem;margin:.25rem 0 .35rem;line-height:1.35;}
.sc .meta{font-family:'IBM Plex Mono',monospace;color:var(--ac);font-size:.72rem;}
#MainMenu,footer,header{visibility:hidden;}
</style>"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RENDER HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def tbadge(t):
    tl = t.lower()
    if tl.startswith("reg"): return '<span class="b br">Regulation</span>'
    if tl.startswith("dir"): return '<span class="b bd">Directive</span>'
    return '<span class="b bp">Proposal</span>'

def fbadge(f):
    return '<span class="b by">In Force</span>' if f else '<span class="b bn">Pending</span>'

def render_act(a):
    pvs = "".join(f'<div class="pv">{p}</div>' for p in a["key_provisions"])
    st.markdown(f"""<div class="abox">
{tbadge(a["type"])}<span class="b bc">{a["category"]}</span>{fbadge(a["in_force"])}
<h3>{a["name"]}</h3>
<div class="meta">CELEX: {a["celex"]} &middot; Year: {a["year"]}</div>
<div class="sl">What This Act Does</div>
<p>{a["summary"]}</p>
<div class="sl">What It Means In Practice</div>
<div class="ex">{a["what_it_means"]}</div>
<div class="sl">Key Provisions</div>
{pvs}
<div class="af">&#128101; <b>Who it affects:</b> {a["who_it_affects"]}</div>
<a class="ll" href="{celex_url(a['celex'])}" target="_blank">&#128196; Full Text on EUR-Lex</a>
<a class="ll" href="{summary_url(a['celex'])}" target="_blank" style="margin-left:6px;">&#128203; Legislative Summary</a>
</div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN APP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    st.set_page_config(page_title="EU Medical Acts Explorer", page_icon="🇪🇺", layout="wide", initial_sidebar_state="expanded")
    st.markdown(CSS, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown('<div style="font-family:Playfair Display,serif;color:#fff;font-size:1.15rem;">🇪🇺 EU Medical Acts</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:IBM Plex Mono,monospace;color:#7e92ad;font-size:.68rem;margin-bottom:.8rem;">EU Commission</div>', unsafe_allow_html=True)
        page = st.radio("Navigate", ["Browse Acts", "SPARQL Search", "CELEX Lookup", "About"], label_visibility="collapsed")
        st.markdown("---")
        st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:.63rem;color:#556b8a;line-height:1.9;"><b>Endpoint</b><br>publications.europa.eu/webapi/rdf/sparql<br><br><b>Ontology</b> CDM (OWL)<br><b>Classifier</b> EuroVoc<br><br>© 2026 Shubhojit Bagchi<br>PhD Research · Ireland</div>', unsafe_allow_html=True)

    # Banner
    st.markdown("""<div class="banner">
<div class="stars">★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★</div>
<div class="sub">©️ Shubhojit Bagchi. All Rights Reserved.</div>
<h1>EU Medical Acts Explorer</h1>
<div class="desc">Browse, search, and understand EU medical legislation — medical devices, pharmaceuticals, clinical trials, health data, blood safety, and patient rights. Click any act to read its full explanation.</div>
</div>""", unsafe_allow_html=True)

    # ── BROWSE ACTS ──
    if "📚" in page:
        c1,c2,c3,c4 = st.columns(4)
        for col,(n,l) in zip([c1,c2,c3,c4],[(len(MEDICAL_ACTS),"Total Acts"),(sum(1 for a in MEDICAL_ACTS if a["type"]=="Regulation"),"Regulations"),(sum(1 for a in MEDICAL_ACTS if a["type"]=="Directive"),"Directives"),(len(CATEGORIES),"Categories")]):
            col.markdown(f'<div class="st"><div class="n">{n}</div><div class="l">{l}</div></div>', unsafe_allow_html=True)

        st.markdown("")
        f1,f2,f3 = st.columns([2,2,1])
        with f1:
            sel_cat = st.multiselect("Filter by Category", CATEGORIES, default=[], placeholder="All categories")
        with f2:
            sel_type = st.multiselect("Filter by Type", ["Regulation","Directive","Proposal"], default=[], placeholder="All types")
        with f3:
            sort = st.selectbox("Sort", ["Newest First","Oldest First","A → Z"])

        acts = [a for a in MEDICAL_ACTS
                if (not sel_cat or a["category"] in sel_cat)
                and (not sel_type or a["type"] in sel_type)]

        if sort == "Newest First": acts.sort(key=lambda a: a["year"], reverse=True)
        elif sort == "Oldest First": acts.sort(key=lambda a: a["year"])
        else: acts.sort(key=lambda a: a["name"])

        st.caption(f"Showing {len(acts)} of {len(MEDICAL_ACTS)} acts — click any act below to expand its full explanation")

        if not acts:
            st.info("No acts match your filters. Try broadening your selection.")

        for i, act in enumerate(acts):
            icon = "🟢" if act["in_force"] else "🟡"
            label = f'{icon} **{act["name"]}** — _{act["type"]}_ ({act["year"]}) · {act["category"]}'
            with st.expander(label, expanded=False):
                render_act(act)
                st.markdown("")
                if st.button("🌐 Fetch Live CELLAR Metadata", key=f"cellar_{act['celex']}_{i}"):
                    with st.spinner("Querying CELLAR SPARQL..."):
                        rows = sparql_celex(act["celex"])
                    if rows:
                        subs = sorted(set(r.get("subj","") for r in rows if r.get("subj")))
                        auths = sorted(set(r.get("author","") for r in rows if r.get("author")))
                        st.markdown('<span class="b ba">✓ CELLAR SPARQL</span>', unsafe_allow_html=True)
                        if subs: st.write(f"**EuroVoc Subjects:** {', '.join(subs[:12])}")
                        if auths: st.write(f"**Author(s):** {', '.join(auths[:5])}")
                        if rows[0].get("date"): st.write(f"**Date:** {rows[0]['date'][:10]}")
                    else:
                        st.info("Could not retrieve additional metadata.")

    # ── SPARQL SEARCH ──
    elif "🔍" in page:
        st.markdown("""<div class="abox"><h3>Live SPARQL Search</h3>
<p>Query the CELLAR endpoint to discover EU health legislation. Filtered by 11 EuroVoc health concepts.</p>
<span class="b ba">SPARQL 1.1</span><span class="b ba">CDM</span><span class="b ba">EuroVoc</span></div>""", unsafe_allow_html=True)

        s1,s2,s3 = st.columns([3,2,1])
        with s1: qt = st.text_input("Search titles", placeholder="e.g. medical device, blood, clinical")
        with s2: qr = st.selectbox("Type", ["Any","Regulation","Directive"])
        with s3: ql = st.number_input("Limit", 5, 100, 25, 5)

        go = st.button("🚀 Execute SPARQL Query", type="primary", use_container_width=True)

        # Store results in session state so they persist
        if go:
            tm = {"Any":"any","Regulation":"regulation","Directive":"directive"}
            with st.spinner("Querying CELLAR SPARQL endpoint..."):
                st.session_state["sparql_results"] = sparql_search_health(qt, tm[qr], ql)

        results = st.session_state.get("sparql_results", None)
        if results is not None:
            if results:
                st.success(f"✓ {len(results)} results from CELLAR")
                for j, r in enumerate(results):
                    cx = r.get("celex","")
                    ti = r.get("title", f"EU Act — {cx}")
                    dt = r.get("date","")[:10] if r.get("date") else ""
                    fo = r.get("force","")
                    tt = r.get("type","").split("/")[-1]
                    tb = '<span class="b br">'+tt+'</span>'
                    fb = ""
                    if fo:
                        fb = '<span class="b by">In Force</span>' if "true" in fo.lower() else '<span class="b bn">Not In Force</span>'
                    st.markdown(f"""<div class="sc">{tb}{fb}
<h4>{html_mod.escape(ti[:250])}</h4>
<div class="meta">CELEX: {cx}{f" · {dt}" if dt else ""}</div>
<a class="ll" href="{celex_url(cx)}" target="_blank">📄 EUR-Lex</a></div>""", unsafe_allow_html=True)

                    # If this is a curated act, offer to show the explanation
                    match = [a for a in MEDICAL_ACTS if a["celex"] == cx]
                    if match:
                        with st.expander(f"📖 Read explanation: {match[0]['name']}", expanded=False):
                            render_act(match[0])
            else:
                st.warning("No results. Try different keywords or a broader type filter.")
        else:
            st.markdown("""<div style="font-family:Source Sans 3,sans-serif;color:var(--mu);font-size:.87rem;margin-top:1rem;line-height:1.7;">
<b>Tip:</b> Leave the search empty and click Execute to browse all recent health legislation. Or try keywords like "device", "blood", "pharmaceutical", "clinical".</div>""", unsafe_allow_html=True)

    # ── CELEX LOOKUP ──
    elif "📖" in page:
        st.markdown("""<div class="abox"><h3>CELEX Lookup</h3>
<p>Enter any CELEX number to fetch metadata from CELLAR. If it's in our database, you'll see the full explanation.</p></div>""", unsafe_allow_html=True)

        l1,l2 = st.columns([3,2])
        with l1: ci = st.text_input("CELEX Number", placeholder="e.g. 32017R0745")
        with l2:
            st.markdown("**Quick pick:**")
            qp = st.selectbox("Known acts", [""] + [f"{a['celex']} — {a['name']}" for a in MEDICAL_ACTS[:10]], label_visibility="collapsed")
            if qp: ci = qp.split(" — ")[0]

        if ci and st.button("🔎 Fetch from CELLAR", type="primary"):
            with st.spinner("Querying..."):
                rows = sparql_celex(ci.strip())
            if rows:
                r0 = rows[0]
                ti = r0.get("title", f"EU Act — {ci}")
                dt = r0.get("date","")[:10] if r0.get("date") else "N/A"
                tt = r0.get("type","").split("/")[-1]
                fo = r0.get("force","")
                fb = '<span class="b by">In Force</span>' if fo and "true" in fo.lower() else '<span class="b bn">Not In Force</span>' if fo else ""
                subs = sorted(set(r.get("subj","") for r in rows if r.get("subj")))
                auths = sorted(set(r.get("author","") for r in rows if r.get("author")))

                st.markdown(f"""<div class="abox">
<span class="b br">{tt}</span>{fb}<span class="b ba">✓ CELLAR</span>
<h3>{html_mod.escape(ti[:300])}</h3>
<div class="meta">CELEX: {ci} · Date: {dt}</div></div>""", unsafe_allow_html=True)

                if subs:
                    st.markdown("**EuroVoc Subjects:** " + " ".join(f'<span class="b bc">{s}</span>' for s in subs[:15]), unsafe_allow_html=True)
                if auths:
                    st.write(f"**Author(s):** {', '.join(auths[:5])}")

                match = [a for a in MEDICAL_ACTS if a["celex"] == ci.strip()]
                if match:
                    st.markdown("---")
                    st.subheader("📖 Full Explanation")
                    render_act(match[0])
                else:
                    st.info("This act is not in our curated database. Read the full text via the links below.")

                st.markdown(f'<a class="ll" href="{celex_url(ci.strip())}" target="_blank">📄 Full Text</a><a class="ll" href="{summary_url(ci.strip())}" target="_blank" style="margin-left:6px;">📋 Summary</a>', unsafe_allow_html=True)
            else:
                st.error(f"No results for CELEX: {ci}. Check format (e.g. 32017R0745).")

    # ── ABOUT ──
    elif "ℹ️" in page:
        st.markdown("""<div class="abox"><h3>About</h3>
<div class="sl">Purpose</div>
<p>Makes EU medical legislation accessible. Each act has four explanation layers: what it does, what it means in practice, key provisions, and who it affects.</p>
<div class="sl">Architecture</div>
#<p><b>Data:</b> CELLAR (Publications Office) · <b>Query:</b> SPARQL 1.1 · <b>Ontology:</b> CDM (OWL) · <b>Filter:</b> EuroVoc (11 health concepts) · <b>Frontend:</b> Streamlit · <b>Auth:</b> None (public API)</p>
#<div class="sl">EuroVoc Concepts</div>
<p style="font-family:IBM Plex Mono,monospace;font-size:.78rem;color:var(--ac);">3885 (health policy) · 3730 (pharmaceutical) · 192 (medical device) · 4636 (public health) · 5765 (health legislation) · 5932 (clinical trial) · 1919 (medicinal product) · 1854 (health care) · 4584 (medical research) · 3371 (blood) · 4587 (patient's rights)</p>
<div class="sl">Disclaimer</div>
<p>Research tool, not affiliated with the EU. Always refer to official EUR-Lex texts for authoritative legal content.</p></div>""", unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;margin-top:2rem;font-family:Source Sans 3,sans-serif;color:var(--mu);font-size:.78rem;">Built with Streamlit · EUR-Lex CELLAR SPARQL<br>© 2026 Shubhojit Bagchi · PhD Research · Ireland</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
