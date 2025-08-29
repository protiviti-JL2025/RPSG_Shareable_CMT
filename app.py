import streamlit as st
from io import BytesIO
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pandas as pd
from datetime import datetime
from streamlit_quill import st_quill
import openpyxl
import re  # <-- for stripping HTML before writing to .docx

# =========================
# CLAUSES LIBRARIES
# =========================
CLAUSES_NDA = {
    1: """1. In this Agreement except where the context otherwise requires:

(a) In this Agreement the terms listed below shall have the following meanings:

“Affiliate”) means with respect to any Party any Person which, directly or indirectly, (a) Controls such Party, (b) is Controlled by such Party, (c) is Controlled by the same Person who, directly or indirectly, Controls such Party. 

“Agreement” means this Agreement, as may be amended from time to time.
“Applicable Law” means applicable laws, by-laws, rules, regulations, orders, ordinances, protocols, codes, guidelines, policies, notices, directions, judgments, decrees or other requirements or official directive of any Governmental Authority or Person acting under the authority of any Governmental Authority, as applicable to the Parties, as the case may be.

“Confidential Information” includes any written information, content and data shared by the Disclosing Party, whether relating to business idea, operating models, cost plans, customer lists, vendor details, marketing plans, launch plans, know-how, methodology or data, in any written form or medium, tangible or intangible, used in or relating to the assets, properties, business activities, or operations of the Disclosing Party and/or its Affiliates, which is disclosed in writing by the Disclosing Party and/or its representatives to the Receiving Party and/or its representatives, in any written form or media. An illustrative list of Confidential Information is set out below:
a) any information relating to future and proposed plans, processes, products, services and sales, including but not limited to, the information that is shared with the Receiving Party and/or its Representatives or that the Receiving Party or their Representatives come across during the course of this Agreement;

b) any information relating to the business, affairs, practices or methods, services, operational processes, marketing activities, technical know–how, administrative and/or organizational matters relating to the Disclosing Party and/or its Affiliates provided by the Disclosing Party and/or its Affiliates or their Representatives, customer data, vendor details, in particular, names, addresses of its present or prospective investors or target companies/firms;

c) information of a business nature, such as financial statements, marketing plans, business plans, strategies, forecasts, unpublished financial information, budgets, projections, information, and data concerning costs, profits, market share, sales, current or planned distribution methods and processes, target company/firm lists, market studies, business plans, or information regarding, investors or lenders of the Disclosing Party and/or its Affiliates;

d) any other information obtained from the Receiving Party and/or its Representatives in relation to the Disclosing Party, which otherwise fall within the scope of this definition of “Confidential Information.
“Control” means with respect to any Person, means: (a) the possession, directly or indirectly, of the power to direct or cause the direction of the management and policies of such Person whether through the ownership of voting securities, by agreement or otherwise or the power to elect more than one-half of the directors, partners or other individuals exercising similar authority with respect to such Person, or (b) the possession, directly or indirectly, of a voting interest of equal to or more than 50% (Fifty Percent) in a Person.

“Disclosing Party”, shall mean, RPSG Ventures Limited and its officers, agents and other persons engaged by the Company for the purpose of this agreement
“Governmental Authority” shall mean any nation or government or any province, state or any other political subdivision thereof; any entity, authority or body exercising executive, legislative, judicial, regulatory or administrative functions of or pertaining to government, including any government authority, agency, department, board, commission or instrumentality of India or any other country, state or jurisdiction.
"Representative" means, as to any Person, such Person's affiliates and its and their respective directors, officers, members, employees, agents, partners, financing providers, co-investors, investors, consultants, advisors (including, without limitation, financial advisors, counsel and accountants) and controlling Persons.
“Receiving Party”, shall mean ______________ including its  officers, agents and other persons engaged by the Company for the purpose of this agreement.

“Third Party” shall mean any Person other than the Receiving Party or Disclosing Party not being a Party to this Agreement.""",
    2: """2. The Receiving Party agrees that all written information disclosed by the Disclosing Party Group pursuant to this Agreement shall be considered Confidential Information, unless otherwise specified in writing by the Disclosing Party. By executing this Agreement, the Receiving Party acknowledges that the Disclosing Party derives independent economic value from the Confidential Information not being generally known and that the disclosure of the Confidential Information is subject to the Receiving Party keeping such information in confidence. The Receiving Party shall inform each of its Representatives to whom it intends to disclose Confidential Information in accordance with this Agreement that the obligations imposed on the Disclosing Party in relation to the Confidential Information shall apply in the same manner to such Representatives.""",
    3: """3. Non-disclosure Obligations. The Receiving Party shall utilize the Confidential Information provided by any Disclosing Party Group member exclusively for the Business Purpose and shall not disclose, publish or disseminate (except with the prior written consent of the Disclosing Party) any Confidential Information to any Third Party other than its Representatives and such other persons whom the Disclosing Party grants its express written consent for disclosure of Confidential Information, who shall be necessarily required to possess such Confidential Information in order for the Receiving Party to fulfil the Business Purpose. Without limiting the generality of the foregoing, the Receiving Party shall, and shall procure and ensure that each of its Representatives to whom the Receiving Party discloses any Confidential Information in accordance with this Agreement shall:

A. Hold such Confidential Information in strict confidence and take commercially reasonable precautions and adequate measures to protect and safeguard the Confidential Information against unauthorized use, publication or disclosure.

B. Not use any of the Confidential Information except in furtherance of the Business Purpose.

C. Not, directly or indirectly, in any way, disclose any of the Confidential Information to any person except as specifically authorized by the Disclosing Party in accordance with this Agreement.

Restrict the access to all Confidential Information by the Representatives on a strictly “need to know” basis for the performance of their duties in furtherance of the Business Purpose.""",
    4: """4. Exceptions. The confidentiality obligations hereunder shall not apply to Confidential Information which (i) is or later becomes public knowledge, except as a result of any unauthorised disclosure by the Receiving Party or its Representatives pursuant to this Agreement; or (ii) was rightfully in possession of the Receiving Party or its Representatives, on a non-confidential basis, prior to its receipt thereof from any Disclosing Party Group member as can be reasonably demonstrated by the Receiving Party via written records, or (iii) is independently developed by the Receiving Party or its Representatives without the use of any Confidential Information as can be reasonably demonstrated by the Receiving Party via written records.""",
    5: """5. Return of Confidential Information. Upon the written request of the Disclosing Party or termination of this Agreement, whichever is the earlier, the Receiving Party shall, and shall procure and ensure that each of its Representatives shall, within 14 days thereafter deliver to the Disclosing Party all records, notes, and other written, printed, or tangible materials either in soft or hard copy form which is in the possession of the Receiving Party or its Representatives, embodying or pertaining to the Confidential Information. The Receiving Party shall promptly notify the Disclosing Party following completion of the foregoing obligation. Notwithstanding the foregoing, the Receiving Party and its Representatives (i) may retain copies of the Confidential Information to the extent that such retention is required to demonstrate compliance with applicable law, rule, regulation or professional standards, or to comply with a bona fide document retention policy, provided, however, that any such information so retained shall be held in compliance with the terms of this Agreement for a period of 7 (seven) years from the date of this Agreement and (ii) shall, to the extent that (i) above is inapplicable to Confidential Information that is electronically stored, destroy such electronically stored Confidential Information only.""",
    6: """6. Unpublished Price Sensitive Information. The Receiving Party acknowledges that, in connection with and in furtherance of the Proposed Transaction, the Receiving Party may receive Confidential Information which may contain unpublished price sensitive information (UPSI) as defined under the SEBI (Prohibition of Insider Trading) Regulations, 2015, as amended from time to time. Each Party represents that it is aware of the securities laws prevalent in India, including the SEBI (Prohibition of Insider Trading) Regulations, 2015, as amended from time to time and the respective parties shall be responsible for compliance with such laws in respect of receipt and use of UPSI.""",
    7: """7. No Representation or Warranty. Except as maybe provided in a definitive agreement between the Parties in connection with the Proposed Transaction, the Disclosing Party does not make any representation or warranty as to the accuracy or completeness of the Confidential Information or of any other information provided, or as to the reasonableness of any assumptions on which any of the same is based, to the Receiving Party or its Representatives, and accordingly, the Receiving Party agrees that the Disclosing Party Group and any of its directors, officers, employees, advisers or agents shall have no liability towards the Receiving Party which may result from the Receiving Party’s unauthorized, use, disclosure or possession of the Confidential Information nor for any claims of Third Parties or as a result of their reliance on any Confidential Information nor for any opinions, projections or forecasts expressed or made by them nor for any errors, omissions or mis-statements made by any of them, and agrees that the Confidential Information is subject to change without notice at any time. In furnishing any Confidential Information no obligation is undertaken by the Disclosing Party to provide any additional information.""",
    8: """8. No grant of any right, title, or interest in the Confidential Information. The Confidential Information, including without limitation any patents, copyrights, trademarks, or other intellectual property rights (present or future) in such Confidential Information, shall at all times remain the sole and exclusive property of the Disclosing Party Group. In no situation whatsoever, shall the Receiving Party have any title, right, interest, or claim over such Confidential Information.""",
    9: """9. Compelled Disclosure. Pursuant to any Applicable Law, if the Receiving Party or any of its Representatives receives any notice or order by any judicial, Governmental Authority or regulatory entity to disclose any or all Confidential Information, then the Receiving Party shall, and shall procure that such Representatives shall, (to the extent permitted by Applicable Law) make reasonable efforts to promptly notify the Disclosing Party so that the Disclosing Party has the opportunity to intercede and contest such disclosure and the Receiving Party shall, and shall procure that such Representatives shall, wherever reasonably required, cooperate with the Disclosing Party in contesting such a disclosure. The Receiving Party shall, and shall procure that such Representatives, furnish only such part of the Confidential Information that the Receiving Party or such Representatives are legally compelled to disclose to the extent legally permissible.""",
    10: """10. No Trade Obligation: Notwithstanding anything contained in this Agreement, the Receiving Party agrees that neither the Receiving Party or its Affiliates shall acquire any interest (whether economic or otherwise) in the Company, other than by way of the Proposed Transaction, for a period of 6 (six) months from the date of this Agreement.""",
    11: """11. Losses. The prevailing Party in any dispute between the Parties shall be entitled to recover its reasonable costs and expenses (including their attorney’s fees and costs) in connection with such action.""",
    12: """12. Notices: Any notice, request or instruction to be given hereunder by any Party to the other Party shall be in writing, in English language and delivered personally, or sent by registered mail postage prepaid or courier or electronic mail addressed to the concerned Party at the address set forth below or any other address subsequently notified to the other Parties.

Company: 
Address:         RPSG House, 2/4, Judges Court Road,
Kolkata 700027, West Bengal
Attention:      Legal Department 
Email Address:  [•]

For receiving party
Address:        [•]
Attention: Mr.  [•]
Email Address:  [•]

Any notice, request or instruction: (i) sent by email, shall be deemed received when sent; (ii) sent by hand, shall be deemed received when delivered; or (iii) sent by post, shall be deemed received 48 hours after posting.""",
    13: """13. Counterparts. This Agreement may be executed in two counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument.""",
    14: """14. Term and Termination. If either Party decides not to proceed with the Business Purpose with the other Party, it shall notify the other Party in writing immediately (such notice, a “Termination Notice”). This Agreement shall commence on the Execution Date and remain in full effect until earlier of: (a) execution and delivery of the definitive agreements regarding the Proposed Transaction; or (b) 24 months from the Execution Date.""",
    15: """15. Remedies. The Receiving Party understands and acknowledges that any disclosure or misappropriation of any of the Confidential Information in violation of this Agreement may cause the Disclosing Party Group irreparable harm, the amount of which may be difficult to ascertain and, therefore, agrees that the Disclosing Party shall have the right to apply to a court of competent jurisdiction for an order restraining any such further disclosure or misappropriation and for such other relief as the Disclosing Party shall deem appropriate. Such right of the Disclosing Party shall be in addition to any other remedies available to the Disclosing Party at law or in equity.""",
    16: """16. Non-Disclosure by the Company. Except as required by law, regulation, legal process or any court order, without the Receiving Party prior written consent, the Company and its respective Representatives shall not, directly or indirectly, identify the Receiving Party or its affiliates by name or identifiable description as being involved in discussions or negotiations concerning the Proposed Transaction, or disclose any of the terms, conditions, work product or analysis prepared or submitted by the Receiving Party in connection therewith, to any person other than a Representative of the Company who reasonably requires access to such information in connection with the Proposed Transaction.""",
    17: """17. Entire Agreement. This Agreement embodies the entire understanding between the Parties relating to the subject matter of this Agreement and supersedes any and all prior negotiations, correspondence, understandings and agreements between the Parties relating to the subject matter of this Agreement. This Agreement shall not be modified except by a writing duly executed by authorized representatives of all Parties. Should any provision of this Agreement be found unenforceable, such provision or part thereof, to the minimum extent required, shall be deemed to be deleted from this Agreement and the validity and enforceability of the remainder of this Agreement shall still be in effect.""",
    18: """18. No Waiver. The failure of the Disclosing Party to require performance by the Receiving Party of any provision of this Agreement shall in no way effect the full right to require such performance at any time thereafter.""",
    19: """19. Assignment. The Receiving Party shall have no right to assign or otherwise transfer, in whole or in part, any of its rights or obligations under this Agreement without obtaining prior written consent from the Disclosing Party.""",
    20: """20. Third Party Rights. Except as expressly provided in this Agreement, no Third Party shall have any right to enforce any term of this Agreement.""",
    21: """21. Governing Law. This Agreement shall be governed by and construed in accordance with the laws of India, without regard to its choice of law provisions and the Courts in Kolkata, India shall have non-exclusive jurisdiction over any dispute hereunder.""",
    22: """22. Amendment. This Agreement constitutes the sole understanding of the Parties about this subject matter and may not be amended or modified except in writing signed by each of the Parties to the Agreement."""
}

# 21 CLAUSES for PURCHASE AGREEMENT (grouped exactly as your draft)
CLAUSES_PA = {
    1: """1. DEFINITIONS:

In this AGREEMENT, the following expressions shall have, where the context so admits, the meanings assigned thereto.

(a) "AGREEMENT" shall mean this document together with appendices hereto if any, and shall include any modifications and alterations hereto made in writing.
(b) "Effective Date" shall mean the date on which the authorised representatives of the parties have duly executed this AGREEMENT.
(c) "Licenses" shall mean clearances, licenses, registrations, nominations and permits required under Food Safety and Standards Act 2006, Food Safety and (Standards Packaging and Labelling) Regulations 2011, Legal Metrology Act 2009 and Legal Metrology (Packaging Commodity) Rules 2011 as on today and/or amended from time to time and/or any other law required to run the business of sale of the food articles.
(d) "Products" shall mean and refer to all type of articles manufactured, processed, supplied, distributed and marketed by the Supplier that had been mutually agreed herein or shall be determined by the Company at a future date, to be supplied at the retail outlets of the Company or at any other place that the Company may demarcate from time to time.
(e) "Parties" shall mean the Company or ___________________ together and party shall mean either Spencer’s Retail Limited or _______________, as the case may be.
(f) "Stores" will mean and include all such Spencer’s stores which are in operation or which may be opened during the Term of this Agreement.""",
    2: """2. SCOPE OF WORK

2.1 The Company shall periodically place purchase orders for the products and the Supplier shall deliver the same to the Company in such manner and at such place as required/intimated by the Company from time to time.

2.2 The Company shall inform the Supplier of the specifications of the products and may ask for the samples prior to such supply and the Supplier shall supply the products strictly as per the specifications as shall be prescribed by the Company.

2.3 The Supplier shall ensure that the products are neatly and cleanly packed in such manner and quantity as required by the Company before supply.

The Supplier shall ensure that each and every package containing the materials/products shall contain the following in the main display panel: (i) identity of the commodity; (ii) accurate number of the commodity contained; (iv) Maximum Retail Price; (v) name and address of the manufacturer; (vi) date when packed and serial number; (vii) contact details in case of consumer dispute; (viii) Veg/Non-Veg logo; (ix) List of ingredients; (x) Nutritional Panel; (xi) Batch number.

In the event of any action being brought against the Company or any penalties being imposed on the Company for failure on the part of the Supplier to conform to applicable laws and regulations:
(a) the Supplier shall indemnify the Company for any loss or damage incurred by the Company as a result of the action or penalty imposed;
(b) the Supplier shall indemnify the Company for all costs, expenses and damages incurred by the Company in any and all proceedings, civil or criminal, that may be brought against the Company for failure to conform to the Packaging Rules;
(c) the Company shall have the option of terminating this Agreement within 10 days of knowledge of the action being brought against the Company, provided such breach on part of the Supplier had not been addressed and/or steps initiated for rectification.

2.4 The Company shall provide the Supplier with the schedule of its requirement sufficiently in advance to enable planning. However, the schedule will be tentative. Supplier shall be ready to comply within the time prescribed by the Company, not exceeding 14 (Fourteen) days from receipt of the purchase/supply request.

2.5 The Supplier shall at all times supply the products to the Company in the exact quantity and manner at the place confirmed by the Company.

2.6 The Supplier shall maintain a system of ‘traceability’.

2.7 Order Cancellation
(a) Any time before scheduled commencement of manufacturing of the products as mentioned in the PO, the Company may cancel the order. No compensation will be paid.
(b) Company may reject and refuse to pay for Products which (i) are not manufactured/packed as per specifications; (ii) are damaged upon receipt; (iii) are not in compliance with this Agreement.

2.8 RISK IN TRANSIT: Manufacturer shall be solely responsible for all risk and damages during transit until received by the Company or its designee. Any transit/freight claims shall be handled by the Manufacturer.""",
    3: """3. PRINCIPAL TO PRINCIPAL BASIS

This AGREEMENT is on a Principal to Principal basis.

a. COMPANY shall not be responsible for any acts/omissions of VENDOR’s personnel working under VENDOR’s supervision.
b. COMPANY and VENDOR are independent parties; nothing herein creates JV, partnership, agency, consultancy or employment.""",
    4: """4. PRICE & PAYMENT

4.1 Prices as per annexure; any change to be intimated at least 30 days in advance.

4.2 Price payable = invoice price minus margin/discounts offered by Supplier; inclusive of all taxes, duties, cess and deliveries, borne by Supplier.

4.3 Payment within period specified in Annexure from receipt of goods, unless defects/damages/pilferages/complaints/claims arise within that period.""",
    5: """5. RIGHTS AND DUTIES OF THE SUPPLIER

5.1 Diligently carry out the work; improve quality, reduce cost, improve productivity.
5.2 Carry out supply strictly as per statutory provisions and Company checks.
5.3 Inform Company immediately of any quality problem.
5.4 Ensure products and packaging conform to Legal Metrology and FSSAI, etc.
5.5 Ensure no stoppage/delay from accepted schedule.
5.6 Supply FOR DC or FOR retail outlet as per PO terms.
5.7 If unable to adhere to schedule, inform Company; Company may source outside and debit loss/additional cost (excluding force majeure).
5.8 Supplier responsible for GST/levies, etc.
5.9 Obtain and comply with all sanctions/licenses; indemnify Company for non-compliance.
5.10 No child labour in manufacturing/packaging/distribution.""",
    6: """6. CONSIDERATION

6.1 Supplier has agreed to pay/allow consideration and credit terms as in annexure.""",
    7: """7. RETURN POLICY

7.1 Company may return non-compliant products within 30 days of receipt; transport cost to Supplier’s account.
7.2 For any consumer quality complaint, Supplier shall replace free of cost and indemnify Company for losses/costs arising therefrom.
7.3 Supplier shall take back unsold non-moving stock from the point of delivery.""",
    8: """8. DAMAGE POLICY

8.1 Supplier shall replace expired product if supplied to Company; no liability for mishandling/improper storage at Company premises.
8.2 Supplier will replace all expired/damaged products as per actual. Both parties will work jointly to reduce expiry/damage.""",
    9: """9. PROMOTION PLAN

9.1 Supplier will provide a quarterly promo calendar, with at least one promotion every month per outlet; special promotions during festivals/regions.
9.2 Supplier will offer consumer promotions for each new outlet for a mutually decided period.""",
    10: """10. RIGHTS AND DUTIES OF THE COMPANY

10.1 Provide specifications/formulations/designs sufficiently in advance.
10.2 Supply schedules and POs to be precise; modifications with Supplier’s consent.
10.3 Pay price as mutually agreed.
10.4 Provide cooperation to improve performance.
10.5 Entitled to reject products not complying with standards; Supplier to replace within 7 days of intimation.
10.6 Supplier to take back rejected stocks within 15 days; during this period Company holds at Supplier’s cost/risk; thereafter costs debited to Supplier.
10.7 Company to share necessary information to enable Supplier’s performance.
10.8 Company may terminate with 4 weeks’ notice; immediate termination for inefficiency/non-compliance/misappropriation, etc.""",
    11: """11. COMPLIANCE OF LEGISLATION

11.1 Supplier shall comply with all applicable laws (FSSAI, Legal Metrology, Labour, PF, ESI, etc.).
11.2 Supplier shall obtain all necessary licenses/permissions at its cost.
11.3 All persons engaged by Supplier are Supplier’s employees; Supplier to comply with labour statutes and ensure no employment claim against Company; includes personnel deputed in stores for promotion.""",
    12: """12. WARRANTY

12.1 Supplier ensures quality manufacturing/packaging under strict checks; complies with applicable law.
12.2 Supplier shall replace products if any quality/manufacturing defect found; provide warranty as per applicable law.
12.3 Supplier shall give proper invoice and warrants that:
(a) duly organized and validly existing;
(b) has power/authority to execute and perform;
(c) corporate actions obtained;
(d) financial capacity;
(e) Agreement is legal/valid/binding;
(f) no conflict with charter/documents/law/agreements;
(g) no actions/proceedings with material adverse effect;
(h) no violations/defaults with material adverse effect; complied with law; no significant liabilities;
(i) representations do not omit material facts;
(j) accepts risk of inadequacy/mistake; Company not liable;
(k) Products are genuine, defect-free, with manufacturer warranty (if any), and meet PO/sample specs.""",
    13: """13. CONFIDENTIALITY

13.1 Parties agree all information obtained under this agreement is confidential and will not be used/shared for any other purpose.
13.2 Logos/trademarks/designs not to be used except as envisaged herein or with prior written consent.
13.3 Supplier shall not assign any part of this agreement without Company’s consent; breach enables immediate termination and damages.""",
    14: """14. INDEMNITY

14.1 Supplier shall indemnify Company against all losses/claims/damages/costs arising from acts/omissions/negligence/breach.
14.2 Supplier specifically indemnifies against claims/fines/penalties arising out of manufacturing defects and/or non-compliance of food laws.
14.3 Supplier shall bear fines/legal fees if required by Company.
14.4 On receipt of any legal notice etc., Company may defend/settle at Supplier’s cost.
14.5 Supplier shall assist in defending; compromise/settlement with mutual agreement.""",
    15: """15. FORCE MAJEURE

15.1 Failure/delay due solely to Force Majeure (act of God, government, riots, war, strikes, lockouts, transport accidents, etc.) shall not be breach, provided the affected party did not cause it, used diligence to avoid/ameliorate, and continues efforts to comply.
15.2 Party suffering Force Majeure shall notify within 7 days and use best efforts to remove/remedy.
15.3 If Force Majeure persists for more than three consecutive months, other party may terminate without liability.""",
    16: """16. TERM AND TERMINATION

16.1 Unless terminated, term is 5 (Five) years from signing.
16.2 Company may terminate without cause by 30 days’ notice.
16.3 Either party may terminate by one month’s notice without reason.

If Supplier cannot provide materials/products within required timeframe, Company may terminate forthwith; Supplier liable for damages due to non-compliance/breach.

Additional grounds for Company’s immediate termination include:
a. Supplier’s failure to perform (save Force Majeure or Company’s sole fault);
b. arrears/unpaid amounts due to Company;
c. false/misleading representations/warranties;
d. illegal/prohibited activities by Supplier or its employees;
e. bankruptcy/insolvency of Supplier;
f. resolution for voluntary winding up;
g. repeated customer grievances on quality;
h. failure to deliver within time;
i. breach of statutory regulations/gross negligence;
j. delivery not matching request, short/excess supply;
k. failure to receive back products despite intimation or after display period.

Additionally, immediate termination if Supplier fails in: (i) Quality; (ii) Service; (iii) Marketing Activities; (iv) Delay in Delivery; (v) Non-acceptance of defective/damaged materials.

After notice period expiry, parties will reconcile accounts within 15 days.""",
    17: """17. QUALITY POLICY

17.1 Supplier shall adhere to standards under Food Laws or other rules; ensure product safety and quality.
17.2 If entire batch is defective, Company may remove from display immediately; cost of goods/logistics debited to Supplier. Supplier to respond within a week with counter-measures, redress complaint and reconcile with aggrieved customer.""",
    18: """18. NOTICES

Any notice/letter required shall be deemed properly served if delivered by RPAD/courier/hand at the addresses mentioned hereinabove.""",
    19: """19. AMENDMENTS & MODIFICATIONS

Any amendment/modification may be initiated by letter from either party; becomes binding when acknowledged/accepted by the other party.""",
    20: """20. INTELLECTUAL PROPERTY RIGHTS

No party shall use the trademark/copyright/IP of the other in any unauthorized manner or in any advertisement/publicity without written permission of the owner.""",
    21: """21. JURISDICTION

The courts of Kolkata shall have jurisdiction over disputes arising out of this agreement."""
}

# ------------------------------------------------
# 1) TEMPLATES
# ------------------------------------------------
NDA_TEMPLATE = """NON-DISCLOSURE AGREEMENT

THIS NON-DISCLOSURE AGREEMENT (this “Agreement”) is entered on {DAY} day of {MONTH} 2025 (“Execution Date”) by and between:

RPSG Ventures Limited, a company incorporated under the laws of India with CIN no. {RPSG_CIN_No}(hereinafter referred to as the “Company/ Disclosing Party”), having a registered office at CESC House, Chowirnghee Square, Kolkata - 700001, West Bengal India (which expression shall, unless repugnant to the context thereof, mean and include its subsidiaries, partners, associates, legal representatives, successors, and permitted assigns);

AND

{Vendor_Name}, a company incorporated under the laws of India with CIN no. {Vendor_CIN_No} and having its registered office at {Vendor_Office}, India. (hereinafter referred to as the “Receiving Party”), (which expression shall, unless repugnant to the context thereof, mean and include its subsidiaries, partners, associates, legal representatives, successors, and permitted assigns).

(both are collectively  referred to as “the Parties”)

WHEREAS:

The Parties are negotiating a possible business transaction referred to below (hereinafter called the “Proposed Transaction”). To facilitate the Proposed Transaction and to evaluate and consider entering into the Transaction, the Disclosing Party shall provide to the Receiving Party the Confidential Information relating to the Company.

The Parties desires to protect its rights and the confidentiality of the Information (as hereinafter defined) and the Parties desire to have access to the Information of the others and set out the terms and conditions to be followed by the Receiving Party with respect to the confidential information.

NOW THEREFORE it is agreed as follows:
"""

PURCHASE_TEMPLATE = """AGREEMENT

THIS AGREEMENT is made and executed at Kolkata on …………………………………………, 202….. between 

M/S. Spencers Retail Limited (formerly known as RP-SG Retail Limited), a Company incorporated under the provisions of the Companies Act, 2013, and having its registered office at Duncan House,   No. 31 Netaji Subhas Road, Kolkata–700001 and Corporate Office at RPSG House, 2/4 Judges Court Road,  Kolkata- 700027 (hereinafter referred to as ‘the Company’ and which term shall, unless repugnant to the context, mean and include all its successors-in-interest and assigns) of the First Part through it Mr…………………, 
AND

<name> (PAN: …………….) son/wife of …………….. aged about ____ years resident of <complete address with Holding No………, Police Station: …………… Post Office: …….., PIN> operating his/her sole proprietorship Business as “………………..”

Or

M/s. …………………, a Partnership Firm, registered under the provisions of the Indian Partnership Act, 1932 bearing registration No. …………… dated …………. (if any), having PAN …………… having its principal place of business at <complete address with Holding No………, Police Station: …………… Post Office: ………, PIN ……..…., District: ……………., State: ……….………, represented herein through its Partners (1) Mr./Ms. ………………… S/D/W/o ………… by faith ……..……, by occupation …………, residing at <complete address with Holding No………, Police Station: …………… Post Office: ………, PIN …….., District: …………, State: …………> and (2) Mr./Ms. ………………… S/D/W/o ………by faith ………, by occupation …………, residing at <complete address with Holding No………, Police Station: …………… Post Office: ………, PIN …….., District: ………, State: …………> duly authorised in this regard by all the other partners vide authorisation letter/certificate dated ………………

Or

………………… LLP, a Limited Liability Partnership, incorporated under the provisions of the Limited Liability Partnership Act, 2008 bearing LLPIN …………., having PAN …………… having its registered office at <complete address with Holding No………, Po-lice Station: …………… Post Office: ………, PIN ……..…., District: ……………., State: ……….………, represented herein through its Designated Partners (1) Mr./Ms. ………………… S/D/W/o ………… by faith ……..……, by occupation …………, residing at <complete address with Holding No………, Police Station: …………… Post Office: ………, PIN …….., District: …………, State: …………> having DPIN: ………… and (2) Mr./Ms. ………………… S/D/W/o ………by faith ………, by occupation …………, resid-ing at <complete address with Holding No………, Police Station: …………… Post Office: ………, PIN …….., District: ………, State: …………> having DPIN: ………… duly au-thorised in this regard by all the other partners vide authorisation letter/certificate dated ………………

Or

………………… Limited OR Private Limited (CIN: ……………………), a Company incorporated / existing under the provisions of the Companies Act, 2013, having PAN ……………. having its Registered Office at <complete address with Holding No………, Police Station: …………… Post Office: ………, PIN ……….., District: …, State: …………> and Corporate Office at <complete address with Holding No………, Police Station: …………… Post Office: ………, PIN ……….., District: …, State: …………> represented herein through its authorized signatory Mr./Ms. ………………… <name and designation> S/D/o ………by faith ………, by occupation …………, residing at <complete address with Holding No………, Police Station: …………… Post Office: ………, PIN …….., District: …, State: …………> duly authorised in this regard vide Board resolution dated   ………………

(herein after referred to as ‘the Supplier’ and which term shall, unless repugnant to the context, mean and include its successors and permitted assigns) of the Second Part

WHEREAS:

A. The Supplier is engaged inter-alia in the business of manufacture, sale, marketing and distribution of “___________________ products” (herein after referred to as the “products”) under ‘__________________’ brand.   

B. The Company is engaged in the business of operating retail stores under the various formats, in India under the brand name “Spencer’s”.

C. The Company proposes to sell through its outlets and otherwise, the products of the Supplier and such other items as may be decided mutually by the parties from time to time.

D. The Company has offered the Supplier to supply the products and the Supplier has accepted the same under the following terms and conditions.

NOW THEREFORE THIS AGREEMENT WITNESSETH AS FOLLOWS:
"""

# ------------------------------------------------
# 2) HELPERS
# ------------------------------------------------
def docx_from_plain_text(plain_text: str, title: str = None) -> BytesIO:
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    if title:
        h = doc.add_paragraph()
        run = h.add_run(title)
        run.bold = True
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        h.runs[0].font.size = Pt(16)
        doc.add_paragraph("")

    for block in plain_text.split("\n"):
        doc.add_paragraph(block)

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def add_heading(doc: Document, text: str, size: int = 16, center=True):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def compose_full_contract(preamble: str, clause_texts: list, parties: list, annexure_note: str) -> str:
    body = [preamble.strip(), ""]
    for t in clause_texts:
        body.append(t.strip())
        body.append("")
    if parties:
        body.append("PARTIES")
        for idx, p in enumerate(parties, 1):
            body.append(f"{idx}. {p}")
        body.append("")
    if annexure_note:
        body.append("ANNEXURE")
        body.append(annexure_note)
        body.append("")
    return "\n".join(body)

# --- helper to strip HTML tags for docx writing (keeps export clean even if clauses come from Quill) ---
def strip_html(x: str) -> str:
    return re.sub(r"<[^>]+>", "", x or "")

def build_docx(
    preamble: str,
    clause_texts: list,
    parties: list,
    annexure_note: str,
    title="AGREEMENT",
    annexure_file=None
) -> BytesIO:
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    add_heading(doc, title.upper(), 18, True)
    doc.add_paragraph(strip_html(preamble.strip()))
    doc.add_paragraph("")

    for t in clause_texts:
        p = doc.add_paragraph()
        ts = strip_html(t.strip())
        if len(ts) >= 2 and ts[:2].isdigit() and "." in ts[:5]:
            first_line = ts.split("\n", 1)[0]
            run = p.add_run(first_line)
            run.bold = True
            remainder = ts[len(first_line):]
            if remainder:
                doc.add_paragraph(remainder)
        else:
            p.add_run(ts)
        doc.add_paragraph("")

    if parties:
        add_heading(doc, "PARTIES", 14, False)
        for idx, ptxt in enumerate(parties, 1):
            doc.add_paragraph(f"{idx}. {strip_html(ptxt)}")

    if annexure_note:
        doc.add_paragraph("")
        add_heading(doc, "ANNEXURE", 14, False)
        doc.add_paragraph(strip_html(annexure_note))

    if annexure_file is not None:
        try:
            df = pd.read_excel(annexure_file)
            doc.add_page_break()
            add_heading(doc, "ANNEXURE – DETAILS", 14, True)
            table = doc.add_table(rows=1, cols=len(df.columns))
            table.style = "Table Grid"
            hdr_cells = table.rows[0].cells
            for j, col in enumerate(df.columns):
                hdr_cells[j].text = str(col)
            for _, row in df.iterrows():
                row_cells = table.add_row().cells
                for j, val in enumerate(row):
                    row_cells[j].text = "" if pd.isna(val) else str(val)
        except Exception as e:
            doc.add_paragraph("")
            doc.add_paragraph(f"[Annexure could not be inserted: {e}]")

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def default_annexure_template() -> BytesIO:
    df = pd.DataFrame(
        columns=["S.No", "Item/Deliverable", "Description", "Quantity", "Unit Price", "Total", "Remarks"]
    )
    out = BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Annexure")
    out.seek(0)
    return out

def default_purchase_annexure_template() -> BytesIO:
    # Keep your local template path as you had
    df = pd.read_excel(r"Purchase_Agreement_Annexure_Fromat_Excel.xlsx")
    out = BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Annexure")
    out.seek(0)
    return out

def df_for_display(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure blanks stay blanks (no None)
    out = df.copy()
    out = out.astype(object)
    out = out.where(pd.notnull(out), "")
    out = out.replace({None: ""})
    return out

def df_for_save(df: pd.DataFrame, numeric_cols: list[str] | None = None) -> pd.DataFrame:
    out = df.copy()
    out = out.replace("", pd.NA)
    if numeric_cols:
        for col in numeric_cols:
            if col in out.columns:
                out[col] = pd.to_numeric(out[col], errors="coerce")
    return out

# ------------------------------------------------
# 3) STREAMLIT APP
# ------------------------------------------------
st.set_page_config(page_title="Interactive Contract Generator", page_icon="📄", layout="wide")
st.title("📄 Interactive Contract Generator")

# GLOBAL STATE
if "workflow" not in st.session_state:
    st.session_state.workflow = "form"  # form → clauses → annexure → preview
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "clause_store" not in st.session_state:
    st.session_state.clause_store = {}   # will be synced per contract type
if "custom_clauses" not in st.session_state:
    st.session_state.custom_clauses = []  # list of {"title":..., "text":..., "approved": True/False}
if "parties" not in st.session_state:
    st.session_state.parties = []
if "annexure_note" not in st.session_state:
    st.session_state.annexure_note = ""
if "annexure_file" not in st.session_state:
    st.session_state.annexure_file = None
if "prev_contract_type" not in st.session_state:
    st.session_state.prev_contract_type = None
    
# ✅ add these two flags here
if "clear_custom_quill" not in st.session_state:
    st.session_state.clear_custom_quill = False
if "clear_cc_title" not in st.session_state:
    st.session_state.clear_cc_title = False

# ------------- selectors -------------
entity = st.selectbox("Entity", ["", "RPSG Ventures", "PCBL", "Spencers Retail", "AquaPharm", "Nature's Basket"])
contract_type = st.selectbox(
    "Contract Type",
    ["", "NDA", "PURCHASE AGREEMENT", "Vendor Agreement", "Service Agreement", "Marketing Agreement",
     "Software License Agreement", "Supply Agreement", "Lease/Rent Agreement", "Leave and License Agreement",
     "Franchise Agreement", "Distribution Agreement", "Manufacturing Agreement", "Employment Agreement",
     "Collaboration Agreement", "MoU/LoI"],
    index=0
)

# --- Reset state when the contract type changes ---
if "last_contract_type" not in st.session_state:
    st.session_state.last_contract_type = contract_type

if contract_type != st.session_state.last_contract_type:
    # Reset clause store depending on contract type
    if contract_type == "NDA":
        st.session_state.clause_store = {i: {"text": CLAUSES_NDA[i], "approved": False} for i in CLAUSES_NDA}
    elif contract_type == "PURCHASE AGREEMENT":
        try:
            st.session_state.clause_store = {i: {"text": CLAUSES_PA[i], "approved": False} for i in CLAUSES_PA}
        except Exception:
            st.session_state.clause_store = {}
    else:
        st.session_state.clause_store = {}

    # Always clear custom clauses & parties when switching contract type
    st.session_state.custom_clauses = []
    st.session_state.parties = []

    st.session_state.last_contract_type = contract_type

# --- Sync clause store whenever type changes (kept, harmless) ---
def sync_clause_store():
    if contract_type == "NDA":
        st.session_state.clause_store = {i: {"text": CLAUSES_NDA[i], "approved": False} for i in CLAUSES_NDA}
        st.session_state.custom_clauses = []
    elif contract_type == "PURCHASE AGREEMENT":
        st.session_state.clause_store = {i: {"text": CLAUSES_PA[i], "approved": False} for i in CLAUSES_PA}
    elif contract_type:
        st.session_state.clause_store = {}
    else:
        st.session_state.clause_store = {}
        st.session_state.custom_clauses = []

if st.session_state.prev_contract_type != contract_type:
    sync_clause_store()
    st.session_state.prev_contract_type = contract_type

st.markdown("---")

# ================ STEP 1: FORM UI ================
if st.session_state.workflow == "form":
    if contract_type == "NDA":
        st.subheader("NDA – Collect 10 Inputs")
        fields = [
            ("DAY", "Signing day (e.g., 21)"),
            ("MONTH", "Signing month (e.g., August)"),
            ("RPSG_CIN_No", "RPSG CIN Number"),
            ("Vendor_Name", "Vendor Company Name"),
            ("Vendor_CIN_No", "Vendor CIN Number"),
            ("Vendor_Office", "Vendor Registered Office Address"),
            ("RPSG_Email", "RPSG Email"),
            ("Vendor_SPOC", "Vendor SPOC Name"),
            ("Vendor_Email", "Vendor Email"),
            ("RPSG_SPOC", "RPSG SPOC Name"),
        ]
        cols = st.columns(2)
        for i, (key, label) in enumerate(fields):
            st.session_state.answers[key] = cols[i % 2].text_input(label, value=st.session_state.answers.get(key, ""))

    elif contract_type == "PURCHASE AGREEMENT":
        st.subheader("Purchase Agreement – Collect Inputs")
        pa_fields = [
            ("Effective_Date", "Effective Date (DD-MM-YYYY)"),
            ("Buyer_Name", "Buyer Name"),
            ("Buyer_Address", "Buyer Address"),
            ("Seller_Name", "Seller Name"),
            ("Seller_Address", "Seller Address"),
            ("Goods_Description", "Goods/Services Description"),
            ("Qty", "Quantity/Scope"),
            ("Unit", "Unit of Measure"),
            ("Unit_Price", "Unit Price / Rate"),
            ("Payment_Terms", "Payment Terms"),
            ("Delivery_Terms", "Delivery/Incoterms"),
            ("Delivery_Schedule", "Delivery Schedule"),
            ("Inspection", "Inspection/Acceptance"),
            ("Warranty", "Warranty"),
            ("Limitation", "Limitation of Liability"),
            ("Termination", "Termination"),
            ("Governing_Law", "Governing Law & Jurisdiction"),
            ("Notices_Email", "Notices Email (Both Parties)"),
        ]
        cols = st.columns(2)
        for i, (key, label) in enumerate(pa_fields):
            st.session_state.answers[key] = cols[i % 2].text_input(label, value=st.session_state.answers.get(key, ""))

    else:
        if contract_type:
            st.info("Proceed to the Clauses step to add your own clauses for this agreement.")
        else:
            st.info("Select an Entity and a Contract Type to begin.")

    left, right = st.columns([1, 1])
    if left.button("Save & Go to Clauses ➡️", use_container_width=True, key="to_clauses_btn"):
        st.session_state.workflow = "clauses"
        st.rerun()
    right.button("Reset Form", on_click=lambda: st.session_state.answers.clear(), use_container_width=True, key="reset_form_btn")

# --- Quick actions for NDA on the form page ---
if st.session_state.workflow == "form" and contract_type == "NDA":
    all_filled = all(st.session_state.answers.get(k, "").strip() for k in
        ["DAY","MONTH","RPSG_CIN_No","Vendor_Name","Vendor_CIN_No","Vendor_Office","RPSG_Email","Vendor_SPOC","Vendor_Email","RPSG_SPOC"]
    )

    st.markdown("### Quick actions (NDA)")
    col_q1, col_q2, col_q3 = st.columns(3)

    data = {k: st.session_state.answers.get(k, "") for k in
            ["DAY","MONTH","RPSG_CIN_No","Vendor_Name","Vendor_CIN_No","Vendor_Office","RPSG_Email","Vendor_SPOC","Vendor_Email","RPSG_SPOC"]}
    preamble = NDA_TEMPLATE.format(**data)

    store = st.session_state.clause_store or {}
    approved = [store[i]["text"] for i in sorted(store) if store[i]["approved"]] if store else []
    if not approved:
        approved = [store[i]["text"] for i in sorted(store)] if store else []

    quick_preview_text = compose_full_contract(
        preamble=preamble,
        clause_texts=approved,
        parties=st.session_state.parties,
        annexure_note=""
    )

    if col_q1.button("👁️ Preview now", key="qa_preview_btn", disabled=not all_filled, use_container_width=True):
        st.markdown("#### Preview")
        st.markdown(quick_preview_text.replace("\n", "<br>"), unsafe_allow_html=True)

    docx_file_quick = build_docx(
        preamble=preamble,
        clause_texts=approved,
        parties=st.session_state.parties,
        annexure_note="",
        title="NON-DISCLOSURE AGREEMENT"
    )

    col_q2.download_button(
        "📥 Download (.docx)",
        data=docx_file_quick,
        file_name="NDA_Final.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        disabled=not all_filled,
        use_container_width=True,
        key="qa_download_btn"
    )

    if col_q3.button("✅ Submit", key="qa_submit_btn", disabled=not all_filled, use_container_width=True):
        st.success("Submitted! (You can wire this to email or your DMS.)")

# =======================
# STEP 2: CLAUSE MANAGER
# =======================
elif st.session_state.workflow == "clauses":
    st.subheader("Clauses – Edit / Rephrase / Approve")
    st.caption("For NDA/Purchase: edit standard clauses and add custom ones. For other types: add custom clauses only.")

    is_std = contract_type in ("NDA", "PURCHASE AGREEMENT")

    # ---------- STANDARD CLAUSES (only NDA / PA) ----------
    if is_std and st.session_state.clause_store:
        selected_keys = sorted(st.session_state.clause_store.keys())
        selected = st.selectbox("Standard clause (pick to edit)", selected_keys, key="clause_select")
        display = st.session_state.clause_store[selected]["text"]

        edited = st_quill(
            value=display,
            placeholder="Edit clause text here...",
            key=f"clause_quill_{selected}",
        )

        c1, c2 = st.columns(2)
        if c1.button("Save Edit", key=f"save_edit_{selected}"):
            if edited is not None:
                st.session_state.clause_store[selected]["text"] = edited
                st.success("Saved.")

        st.session_state.clause_store[selected]["approved"] = st.checkbox(
            "Approved",
            value=st.session_state.clause_store[selected]["approved"],
            key=f"approved_{selected}",
        )

        st.markdown("---")

    # ---------- CUSTOM CLAUSES (ALL CONTRACT TYPES) ----------
    st.markdown("### ➕ Add Custom Clause")

    # Use a contract-type-specific key for the Quill box
    custom_quill_key = f"custom_quill_{contract_type or 'general'}"

    # If the previous click asked us to clear the widgets, do it BEFORE creating them
    if st.session_state.clear_custom_quill:
        st.session_state.pop(custom_quill_key, None)
        st.session_state.clear_custom_quill = False

    if st.session_state.clear_cc_title:
        st.session_state.pop("cc_title", None)
        st.session_state.clear_cc_title = False

    # Now safely create the widgets
    cc_title = st.text_input("Custom Clause Title", key="cc_title")

    cc_body_html = st_quill(
        value=st.session_state.get(custom_quill_key, ""),
        placeholder="Write your custom clause here…",
        key=custom_quill_key,
    )


    add_col1, add_col2 = st.columns([1, 1])
    if add_col1.button("➕ Add Custom Clause", key="add_custom_clause_btn"):
        if cc_title.strip() and cc_body_html and cc_body_html.strip():
            st.session_state.custom_clauses.append(
                {"title": cc_title.strip(), "text": cc_body_html, "approved": True}
            )
            # Set flags so next run clears the widgets BEFORE they are created
            st.session_state.clear_custom_quill = True
            st.session_state.clear_cc_title = True
            st.rerun()


    # Show the custom clauses list
    if st.session_state.custom_clauses:
        st.markdown("#### Added Custom Clauses")
        for idx, c in enumerate(st.session_state.custom_clauses, 1):
            with st.expander(f"{idx}. {c.get('title','Custom Clause')}", expanded=False):
                # Render with HTML so Quill formatting shows in the app
                st.markdown(c.get("text",""), unsafe_allow_html=True)
                # Toggle approved if needed
                c["approved"] = st.checkbox(
                    f"Approved – {c.get('title','Custom Clause')}",
                    value=c.get("approved", True),
                    key=f"cc_approved_{idx}",
                )
                # Remove button
                if st.button(f"❌ Remove", key=f"remove_cc_{idx}"):
                    st.session_state.custom_clauses.pop(idx - 1)
                    st.rerun()

    st.markdown("---")

    # ---------- PARTIES (ALL CONTRACT TYPES) ----------
    st.markdown("### 👥 Parties")
    new_party = st.text_input("Add Party (Name, Role, Address/email optional)", key="party_input")
    cpa, cpb = st.columns(2)
    if cpa.button("Add Party", key="add_party_btn"):
        if new_party.strip():
            st.session_state.parties.append(new_party.strip())
    if cpb.button("Clear Parties", key="clear_parties_btn"):
        st.session_state.parties = []
    if st.session_state.parties:
        st.write("- " + "\n- ".join(st.session_state.parties))

    st.markdown("---")

    # ---------- NAV ----------
    nav1, nav2 = st.columns([1, 1])
    if nav1.button("⬅️ Back to Form", key="clauses_back_form"):
        st.session_state.workflow = "form"
        st.rerun()

    next_label = "Save & Go to Preview ➡️" if contract_type == "NDA" else "Save & Go to Annexure ➡️"
    if nav2.button(next_label, key="clauses_next_btn"):
        st.session_state.workflow = "preview" if contract_type == "NDA" else "annexure"
        st.rerun()

# ========================= STEP 3: ANNEXURE (Excel) =========================
elif st.session_state.workflow == "annexure":
    if contract_type == "NDA":
        st.session_state.annexure_file = None
        st.session_state.annexure_note = ""
        st.session_state.workflow = "preview"
        st.rerun()

    st.subheader("Annexure (Excel)")
    st.caption("Upload an Excel annexure (pricing, scope, deliverables) or download a blank template.")

    file = st.file_uploader("Upload Annexure (.xlsx)", type=["xlsx"], key="annexure_uploader")
    if file:
        st.session_state.annexure_file = file
        if not st.session_state.get("annexure_note"):
            st.session_state.annexure_note = f"Annexure attached: {file.name}"
        st.success(f"Uploaded: {file.name}")

    c1, c2 = st.columns(2)

    if c1.button("Clear Upload", key="annexure_clear_btn"):
        st.session_state.annexure_file = None
        st.info("Annexure upload cleared.")
    no_annexure = c2.checkbox("No annexure for this contract", value=False, key="no_annexure_chk")

    if contract_type == "PURCHASE AGREEMENT":
        template = default_purchase_annexure_template()
    else:
        template = default_annexure_template()
    st.download_button(
        label="Download Blank Annexure Template (.xlsx)",
        data=template,
        file_name="Annexure_Template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="annexure_template_dl"
    )

    # Inline editor only for Purchase Agreement
    if contract_type == "PURCHASE AGREEMENT" and not no_annexure:
        st.markdown("### ✏️ Edit Annexure Inline")
        if st.session_state.annexure_file:
            raw_df = pd.read_excel(st.session_state.annexure_file)
        else:
            raw_df = pd.read_excel(r"Purchase_Agreement_Annexure_Fromat_Excel.xlsx")

        display_df = df_for_display(raw_df)
        edited_df = st.data_editor(
            display_df,
            num_rows="dynamic",
            use_container_width=True,
            key="annexure_editor"
        )

        col1, col2 = st.columns(2)
        if col1.button("💾 Save Edits", key="save_annexure_edits_btn"):
            numeric_cols = ["Quantity", "Unit Price", "Total", "% of Turnover", "Amount per store (Rs)",
                            "Amount per month (Rs)", "Amount per Vendor (Rs)", "Amount per New Store Launch (Rs)",
                            "Amount per  Store  (Rs)", "Rs"]
            cleaned_to_save = df_for_save(edited_df, numeric_cols=numeric_cols)

            out = BytesIO()
            with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
                cleaned_to_save.to_excel(writer, index=False, sheet_name="Annexure")
            out.seek(0)
            st.session_state.annexure_file = out
            st.success("Edits saved! Download & DOCX will include your changes (with blanks kept blank).")

        if col2.button("↩️ Reset Editor", key="reset_annexure_edits_btn"):
            st.session_state.annexure_file = None
            st.info("Editor reset. Please upload again or use default template.")

    st.text_area(
        "Annexure Note (appears in contract)",
        value=st.session_state.annexure_note,
        key="annexure_note_box",
        height=120
    )
    st.session_state.annexure_note = st.session_state.annexure_note_box

    nav1, nav2 = st.columns([1, 1])
    if nav1.button("⬅️ Back to Clauses", key="annexure_back_clauses"):
        st.session_state.workflow = "clauses"
        st.rerun()

    can_proceed = bool(st.session_state.annexure_file) or no_annexure
    if nav2.button("Save & Go to Preview ➡️", key="annexure_next_btn", disabled=not can_proceed):
        if no_annexure:
            st.session_state.annexure_file = None
            st.session_state.annexure_note = ""
        st.session_state.workflow = "preview"
        st.rerun()

# ========================= STEP 4: PREVIEW & EXPORT =========================
elif st.session_state.workflow == "preview":
    st.subheader("Preview, Download, Submit")

    # Build preamble...
    if contract_type == "NDA":
        data = {k: st.session_state.answers.get(k, "") for k in [
            "DAY","MONTH","RPSG_CIN_No","Vendor_Name","Vendor_CIN_No","Vendor_Office",
            "RPSG_Email","Vendor_SPOC","Vendor_Email","RPSG_SPOC"
        ]}
        preamble = NDA_TEMPLATE.format(**data)
        title = "NON-DISCLOSURE AGREEMENT"

    elif contract_type == "PURCHASE AGREEMENT":
        data = {k: st.session_state.answers.get(k, "") for k in [
            "Effective_Date","Company_Representative","Vendor_Name","Vendor_PAN",
            "Vendor_FatherSpouse","Vendor_Age","Vendor_Address","Vendor_Business"
        ]}
        preamble = PURCHASE_TEMPLATE.format(**data)
        title = "PURCHASE AGREEMENT"

    else:
        preamble = f"{contract_type} between parties."
        title = contract_type

    only_approved = st.checkbox("Show only approved clauses", value=False, key="preview_only_approved")

    # --- STANDARD (NDA/PA only) ---
    standard_clauses = []
    if contract_type in ("NDA", "PURCHASE AGREEMENT"):
        store = st.session_state.clause_store or {}
        if only_approved:
            standard_clauses = [store[i]["text"] for i in sorted(store) if store[i]["approved"]]
            if not standard_clauses:
                st.info("No clauses approved yet; showing all clauses instead.")
                standard_clauses = [store[i]["text"] for i in sorted(store)]
        else:
            standard_clauses = [store[i]["text"] for i in sorted(store)]

    # --- CUSTOM (all) ---
    custom_clauses = [
        f"{c.get('title','Custom Clause')}\n{c.get('text','')}"
        for c in st.session_state.custom_clauses
        if c.get("approved", True)
    ]

    # --- MERGE ---
    if contract_type in ("NDA", "PURCHASE AGREEMENT"):
        clause_list = standard_clauses + custom_clauses
    else:
        clause_list = custom_clauses

    annexure_text = "" if contract_type == "NDA" else st.session_state.annexure_note

    preview_text = compose_full_contract(
        preamble=preamble,
        clause_texts=clause_list,
        parties=st.session_state.parties,      # parties always included
        annexure_note=annexure_text,
    )

    st.markdown("### 📑 Preview")
    # Render as HTML so Quill formatting (in custom clauses) shows nicely
    st.markdown(preview_text, unsafe_allow_html=True)

    if contract_type != "NDA" and st.session_state.annexure_file:
        st.markdown("### 📎 Annexure (Preview)")
        annexure_df = pd.read_excel(st.session_state.annexure_file)
        st.dataframe(df_for_display(annexure_df), use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        docx_file = build_docx(
            preamble=preamble,
            clause_texts=clause_list,
            parties=st.session_state.parties,   # parties in the DOCX too
            annexure_note=annexure_text,
            title=title,
            annexure_file=st.session_state.annexure_file
        )
        st.download_button(
            label="📥 Download (.docx)",
            data=docx_file,
            file_name=f"{title.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
            key="preview_download_btn"
        )
    with c2:
        if st.button("👁️ Refresh Preview", key="preview_refresh_btn", use_container_width=True):
            st.rerun()
    with c3:
        if st.button("✅ Submit", key="preview_submit_btn", use_container_width=True):
            st.success("Submitted! (Wire this button to your DMS/email as needed.)")

    b1, b2 = st.columns(2)
    if b1.button("⬅️ Back to Clauses", key="preview_back_clauses"):
        st.session_state.workflow = "clauses"
        st.rerun()
    if contract_type != "NDA" and b2.button("⬅️ Back to Annexure", key="preview_back_annexure"):
        st.session_state.workflow = "annexure"
        st.rerun()
