import streamlit as st
from io import BytesIO
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pandas as pd
from datetime import datetime
from streamlit_quill import st_quill


# =========================
# CLAUSES (1..22) CONTENT
# =========================
CLAUSES = {
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

# --- NEW: PURCHASE AGREEMENT PREAMBLE TEMPLATE ---
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

A.	The Supplier is engaged inter-alia in the business of manufacture, sale, marketing and distribution of “___________________ products” (herein after referred to as the “products”) under ‘__________________’ brand.   

B.	The Company is engaged in the business of operating retail stores under the various formats, in India under the brand name “Spencer’s”.

C.	The Company proposes to sell through its outlets and otherwise, the products of the Supplier and such other items as may be decided mutually by the parties from time to time.

D.	The Company has offered the Supplier to supply the products and the Supplier has accepted the same under the following terms and conditions.

NOW THEREFORE THIS AGREEMENT WITNESSETH AS FOLLOWS:

1.	DEFINITIONS:

In this AGREEMENT, the following expressions shall have, where the context so admits, the meanings assigned thereto.

(a) 	"AGREEMENT" shall mean this document together with appendices hereto if any, and shall include any modifications and alterations hereto made in writing.

(b)	“Effective Date" shall mean the date on which the authorised representatives of the parties have duly executed this AGREEMENT.

(c)	“Licenses" shall mean clearances, licenses, registrations, nominations and permits required under Food Safety and Standards Act 2006, Food Safety and (Standards Packaging And Labelling) Regulations 2011, Legal Metrology Act 2009 and Legal Metrology (Packaging Commodity) Rules 2011 as on today and or amended from time to time and or any other law required to run the business of sale of the food articles. 

(d)	"Products" shall mean and refer to all type of  articles manufactured, processed, supplied, distributed and marketed by the Supplier that had been mutually agreed herein or shall be determined by the Company at a future date,  to be supplied at the retail outlets of the Company or at any other place that the Company may demarcate from time to time.  

(e)	"Parties" shall mean the Company or ___________________together and party shall mean either Spencer’s Retail Limited or _______________-, as the case may be. 
(f)	Stores’ will mean and include all such Spencer’s stores which are in operation or which may be opened during the Term of this Agreement

2.	SCOPE OF WORK

2.1.	The Company shall periodically place purchase orders for the products and the Supplier shall deliver the same to the Company in such manner and at such place as required/intimated by the Company from time to time.

2.2.	 The Company shall inform the Supplier of the specifications of the products and may ask for the samples prior to such supply and the Supplier shall supply the products strictly as per the specifications as shall be prescribed by the Company.

2.3.	 The Supplier shall ensure that the products are neatly and cleanly packed in such manner and quantity as required by the Company before supply.

The Supplier shall ensure that each and every package containing the materials / products shall contain the following in the main display panel:-

(i) 	the identity of the commodity in the package; 
(ii)	the accurate number of the commodity contained in the package; 
(iv)	the Maximum Retail Price. 
(v)	the name and address of the manufacturer. 
(vi)	the date when packed and the serial number
(vii)	the contact details in case of any consumer dispute
(viii)	Veg Logo / Non Veg Logo
(ix)	List of ingredients
(x)	Nutritional Panel
(xi)	Batch number


In the event of any action being brought against the Company or any penalties being imposed on the Company for failure on the part of the Supplier to conform to the Food Safety and Standards Act 2006, Food Safety and (Standards Packaging And Labelling) Regulations 2011, Legal Metrology Act 2009 and Legal Metrology (Packaging Commodity) Rules 2011 or any other law in force from time to time

(a)	the Supplier shall indemnify the Company for any loss or damage incurred by the Company as a result of the action or penalty imposed;

(b)	the Supplier shall indemnify the Company for all costs, expenses and damages incurred by the Company in any and all proceedings, civil or criminal, that may be brought against the Company for failure to confirm to the Packaging Rules;

(c)	the Company shall have the option of terminating this Agreement within 10 days of knowledge of the action being brought against the Company , provided such breach on part of the Supplier had not been addressed to and / or steps initiated for rectification of the same .


2.4.	The Company shall provide the Supplier with the schedule of its requirement sufficiently in advance in order to enable the Supplier to plan its supply schedule in advance. However the schedule will only be tentative and give a broad parameter within which the such request for supply shall be placed by the Company .The Supplier shall prepare and keep itself ready for compliance, delivery and complete performance of such request within such time as shall be prescribed by the Company and at such place , which in no event shall exceed a maximum time limit of 14 ( Fourteen ) days from the date of receipt of such purchase/supply request from the Company . The confirmed purchase orders/supply request shall be given by the Company and the Supplier shall operate on the basis of the said purchase/supply request as shall be placed by the Company. 

2.5.	 The Supplier shall at all times during the subsistence of this AGREEMENT supply the products to the Company in the exact quantity and manner at the place confirmed by the Company.

2.6.	 The Supplier shall maintain a system of ‘traceability’ in order to enable the tracing of exact source of quality problem as well as for tracing any suspected defects as may be informed or detected by the Company or the Supplier itself

2.7.	Order Cancellation

a)	Any time before the scheduled commencement of manufacturing of the products as mentioned in the Purchase order, the Company may cancel the order due to any business exigencies, change in environment,  in that event no compensation will be paid to the manufacturer
b)	Company  may reject and refuse to pay for Products which 

(i)	are not manufactured, packed  as per the specification 
(ii)	Products which are damaged upon  receipt at Company’s designated place 
(iii)	Products which are not in compliance with the terms and conditions of this Agreement.

2.8.	RISK IN TRANSIT

Manufacturer shall be solely responsible for all the risk and damages arising during the course of transit.  All risks and title in the goods shall be solely with the manufacturer till the same is received by the Company or its designated person.  Any claims arised during the course of transit and any freight claims shall be solely handled by the Manufacturer.



3.	PRINCIPAL TO PRINCIPAL BASIS

It is clearly agreed between the parties herein that this AGREEMENT is entered into on a Principal to Principal basis for the benefit of both the parties and a long term relationship between the parties is envisaged hereunder.

a.	It is expressly understood and agreed upon by the Parties to this Agreement that COMPANY shall not be held responsible for any acts and/or omissions of personnel while such personnel are working under the instructions and supervision of VENDOR.
b.	COMPANY and VENDOR are independent parties to this Agreement and nothing contained in this Agreement shall be construed to create any relationship of a joint venture, association of persons, partnership, principal and agent, principal and consultant or employer and employee between the Parties.




4. PRICE & PAYMENT

4.1 	The Company shall pay the Supplier such prices for the products as may be determined from time to time as mentioned in the annexure. Any successive price change from the last communicated prices will have to be intimated to the company at least 30 days in advance of it’s coming into effect.

4.2	The price to be paid by the Company to the Supplier shall be the invoice price of the product minus the margin and other discounts that shall be offered by the Supplier to the Company, to be deducted from such price .Thus the Net Payable amount shall constitute the Price of the products minus the margin and discounts offered by the Supplier to the Company and shall be inclusive of all taxes , duties, cess and deliveries, which shall be borne by the Supplier .

4.3	The Company shall ensure the payment against supply made by the Supplier with in a period as specified in the Annexure from the receipt of goods from the Supplier, unless there be any defect, damages, pilferages, complaints or claims initiated by any person or entity, without limiting to statutory authority, on the Company in respect to such products supplied by the Supplier within the aforesaid period. 


5.	RIGHTS AND DUTIES OF THE SUPPLIER

5.1	The Supplier shall at all times duly and diligently carry out the work as specified in the scope of work herein. The Supplier shall constantly work towards improving the quality, reducing the cost of production and thus improve productivity. 

5.2	The Supplier shall carry out the supply activities strictly as per the specifications/ provisions laid down in the statutes governing the same including the checks prescribed by the Company from time to time.

5.3	The Supplier shall inform the Company of any quality problem immediately upon observing the same.

5.4	The Supplier shall specifically ensure that the products supplied and the packaging used shall conform to the standards/requirements prescribed under the Legal Metrology (Packaged Commodities) Rules, 2011 and Food Safety and Standards Act, 2006 or any other law in force from time to time. 

5.5	The Supplier shall take all necessary action to ensure that there shall be no stoppage/ delay in supply of products from the accepted delivery schedule. 
5.6	All goods must be supplied by the supplier FOR DC or FOR retail outlet depending on the terms of the PO.

5.7	In case the Supplier is not in a position to adhere to the supply schedule, the Supplier shall inform the Company of the same sufficiently in advance and get the approval of the Company. In such an event, the Company shall be at full liberty to source the products from outside and any loss/additional cost/damage whatsoever that may be incurred by the Company on account of such purchase shall be borne by the Supplier excluding force majure conditions.

5.8	The Supplier shall be responsible for the payment of any duty Goods and Service Tax or such other statutory levies, charges, Payments etc as may be imposed from time to time on the manufacture and sale of the products if required under the law.

5.9	The Supplier confirms that it has obtained the requisite sanctions, licenses, permission from the concerned statutory authorities, bodies for carrying out the aforesaid trade and business and that the Supplier shall comply with such provisions as shall be applicable to the nature of its business during the continuation of the agreement .Any act of non-compliance shall lead to termination and the Supplier indemnifies to the Company for all such acts / abstinence.
5.10	The Supplier shall not employ any child labour in any manner either manufacturing or packaging or distribution of the goods.

6. CONSIDERATION 

6.1.	 The Supplier has agreed to pay / allow a consideration and credit terms more fully mentioned in the annexure enclosed here to this agreement. 
	

7.RETURN POLICY

7.1	The Company shall be entitled to return such product that does not comply to the quality standard prescribed under the law or promised at the time of delivery. Any product if found damaged, destroyed, packed not in accordance with the statutory regulations , tampered with or not upto the satisfaction of the Company shall be immediately returned by the Company to the Supplier .However for the said act the Company shall have 30 days’ time from the date of receipt of the said consignment from the Supplier  containing such damaged product .The cost of transportation / courier in regard to the same shall be in the account of the Supplier .

7.2     In case of any quality complaint by the consumer, the Supplier shall replace such product free of cost. The Supplier shall indemnify the Company against all losses, cost that the Company may be exposed to or have to incur on account of any complaint or action initiated by any person /authority due to the Products supplied by the Supplier and offered for sale by the Company at its retail outlets on account of the same not adhering to the standards or promises made or on account of the same violating any Law in force from time to time.

7.3    The supplier shall take back all unsold stock which might pile up due to non-movement of certain SKU’s with respect to others. The same shall be lifted by the supplier from the point where it was delivered.


8.	DAMAGE POLICY

8.1	The Supplier shall replace the expired product, if supplied to the Company but the Supplier shall not be liable for any damages reimbursement due to mishandling/improper storage or non -compliance of directions related to the packages in the godowns / retail stores of the Company. 

8.2	The Supplier will replace all expired and damaged products as per actual. The Company shall co-operate with the field force of the Supplier so that both the parties and their concerned employees, officers and staff work jointly in order to reduce the expiry & damage level.

9.	PROMOTION PLAN

9.1	The Supplier will provide Promo Calendar Quarterly to the Company with at least one promotion every English calendar month per retail outlet to increase the sales volume of the Company. In addition to the above promotion Special Promotion will be offered by the Supplier in Festivals seasons specific to a particular region or state. 

9.2	The Supplier will offer consumer promotions for each and every new outlet of the Company opening for a specific period as may be mutually decided by the parties herein.

10.	RIGHTS AND DUTIES OF THE COMPANY

10.1	The Company shall provide the specifications, formulations, designs, etc to the Supplier sufficiently in advance in order to enable the Supplier to supply as per the said specifications, formulations, designs, etc.

10.2	That all supply schedules and purchase orders are to be made available to the Supplier in clear and precise terms as contained in the AGREEMENT and in case of any change or modification in the purchase order the same shall be done with prior consent of the Supplier.

10.3	The Company shall pay for the price of the products to the Supplier in such manner as mutually agreed herein or as may be agreed upon between the parties herein from time to time. 

10.4	The Company shall provide wherever possible, all necessary cooperation to the Supplier in order to enable the Supplier to improve the performance.

10.5	The Company shall be entitled to reject the products wherever they are not complying with the standards approved by the Company under the prevailing food laws. The Supplier shall be provided an opportunity to check the stock before being rejected and the decision of the Company in this regard shall be deemed to be final and binding on the parties. If it is found that rejection is on the quality/manufacturing grounds, the Company shall intimate the Supplier of such rejection and the Supplier shall replace the rejected stock with new stock within a period of 7 ( Seven ) days from the date of receipt of such intimation from the Company.  

10.6	The Supplier shall take back the rejected stocks with in 15 ( Fifteen )  days from the date of intimation. During these 15 ( Fifteen ) days, the Company shall hold the rejected stocks at the cost and risk of the Supplier and the Supplier confirms to indemnify the Company from all costs , claims , actions that may be initiated by any person , authority or entity in respect to such products. In case, the Supplier does not lift the rejected stocks with in 15 ( Fifteen ) days, the expenses or loss which the Company has to incur on account of holding such damaged goods including that of segregation, etc will be debited to the account of the Supplier and shall be recovered from and out of the Agreement payable to the Supplier.

10.7	The Company shall share with the Supplier all such information, as it deems necessary for the purpose of Supplier fulfilling its obligations as per this agreement effectively.

10.8	Notwithstanding what is provided under this agreement, the Company has all rights to terminate this agreement by giving 4 ( four ) weeks’ notice in writing to the Supplier . The Company shall be entitled to forthwith terminate the AGREEMENT in case the Supplier is not fulfilling the obligations herein efficiently or standards demarcated and prescribed by the Company or there has been any instances of misappropriation of money, materials, losses, etc committed by any employees , agents , officers or staff of the Supplier.

11.	COMPLIANCE OF LEGISLATION

11.1	The Supplier shall ensure at all times that it shall comply with all requirements set forth under any law, statute, rules, regulations including but not limited Food Safety and Standards Act 2006, Food Safety and Standards (Packaging And Labelling) Regulations 2011, Legal Metrology Act 2009 and Legal Metrology (Packaged Commodities) Rules 2011, Labour Law, Provident Fund and Employee State Insurance Act etc. as may be in force in India from time to time for the discharge of scope of work and manufacture of the products, as envisaged herein.

11.2	The Supplier shall obtain all necessary licenses, permissions, etc required under law or bye law for manufacturing, selling and delivering the products as required under this AGREEMENT, at its own cost.
11.3	It is specifically agreed herein that all the persons employed by the Supplier for supplying the products directly or indirectly shall at all times be the employees of the Supplier. It shall be the duty of the Supplier to comply with requirements prescribed under various labour statutes like PF, ESI, Minimum Wages, maintenance of registers, etc. any penalty imposed on account of not maintaining the above shall be exclusively borne by the supplier. The supplier shall ensure that there shall be no claim of employment with the company by any of the persons engaged by the supplier for supplying the products and those employees/ personnel who are deputed by the supplier to man the bays or aisles in the company’s outlets for the purpose of sales promotion activities”.

12.	WARRANTY

12.1	The Supplier ensures that every possible care is taken during the manufacturing and/or packaging process of the products and the products are manufactured by qualified and experienced staff under various strict quality checks at several points in the factories. The Supplier being a law abiding Company complies the provisions of required law under various enactments. 

12.2	The Supplier shall replace the products if any quality or manufacturing defect found in the products. Further the Supplier assures to give warranty in such form and manner as has been set forth in any Act or Rule applicable for the products from time to time. 

12.3	The Supplier shall give the Company a proper invoice for all the supplies made giving therein all the particulars of the products and also warrants that :-

a.	It is duly organized, validly existing and in good standing under the laws of India;
b.	It has full power and authority to execute, deliver and perform its obligations under this Agreement and to carry out the transactions contemplated hereby;
c.	It has taken all necessary corporate and other action under Applicable Laws and its constitutional documents to authorize the execution, delivery and performance of this Agreement;
d.	It has the financial standing and capacity to execute the agreement;
e.	This Agreement constitutes its legal, valid and binding obligation enforceable against it in accordance with the terms hereof;
f.	The execution, delivery and performance of this Agreement will not conflict with, result in the breach of, constitute a default under or accelerate performance required by any of the terms of the Supplier Memorandum and Articles of Association or any Applicable Law or any covenant, agreement, understanding, decree or order to which the Supplier is a party or by which Supplier or any of its properties or assets are bound or affected;
g.	There are no actions, suits, proceedings or investigations pending or to The Supplier’s knowledge threatened against the Supplier at law or in equity before any court or before any other judicial, quasi-judicial or other authority, the outcome of which may constitute the Supplier Event of Default or which individually or in the aggregate may result in Material Adverse Effect;
h.	It has no knowledge of any violation or default with respect to any order, writ, injunction or any decree of any court or any legally binding order of any government authority, which may result in Material Adverse Effect; It has complied with all applicable law and has not been subject to any fines, penalties, injunctive relief or any other civil or criminal liabilities which in the aggregate have or may have Material Adverse Effect;
i.	No representation or warranty by the Supplier contained herein or in any other document furnished by the Supplier to the Company or to any government authority in relation to Applicable Licenses contains or will contain any untrue statement of material fact or omits or will omit to state a material fact necessary to make such representation or warranty 
j.	The Supplier also acknowledges and hereby accepts the risk of inadequacy, mistake or error in or relating to any of the matters set forth above and hereby confirms that the Company shall not be liable for the same in any manner whatsoever to the Supplier
k.	The Products are genuine and free from defects and have the requisite manufacturer warranty (if any) associated with such Product and meet the specifications of the PO/samples


13.	CONFIDENTIALITY  

13.1	That the parties do hereby assure each other and agree that all information, details, documents, etc. which they get in possession by virtue of this agreement are very confidential and they will not permit to share or use for any other purpose whatsoever. 

13.2	The parties further assure that they will not use the logos, trademark, and design of each other for any purpose other than what is envisaged under this agreement except with the express and written consent of each other.    

13.3	The Supplier shall not have the right to assign any part of this agreement to any other third party at any point of time .Any such assignment shall be deemed to be in contravention of this agreement and in such event The Company shall have the right to terminate the agreement with immediate effect, without limiting to its rights to claim damages for such unauthorized assignment. 


14.	INDEMNITY

14.1	The Supplier hereby agree to indemnify the Company against all losses, claims, damage, cost, whatsoever incurred and/or to be incurred by the Company on account of any act of commission or omission or negligence or any such act or breach of the terms and conditions contained herein. 

14.2	The Supplier hereby specifically agree to indemnify the Company against any claims, fine, penalty, award, order, judgment, etc. passed against the parties by any court, forum, authority, etc. arising out of any manufacturing defects and /or non-compliance of standards or requirements prescribed under food laws as may be applicable from time to time. 

14.3	The Supplier shall bear the cost, if required by the Company, towards fine and legal fees for defending the case.  

14.4	Whenever the Company receives any notice, summons, warrant, etc. of any potential claim, suit, complaint, etc., in regard to the products supplied and delivered by the Supplier to the Company, the Company shall be entitled, to take up such defence and engage such counsel of its choice to contest the case or opt for settlement/compromise/compound of the same and all costs, charges for the same shall be payable by the Supplier. 

14.5	The Supplier shall render all possible assistance and cooperation in contesting and defending the case. Any such case / dispute / litigation case may be compromised or settled with mutual agreement of the parties. 

15.	FORCE MAJEURE

15.1	That the failure or delay of any party to perform any obligations under this agreement solely by reason of act of God, acts of Government (except as otherwise enumerated herein), riots, wars, strikes, lockouts, accidents in transportation or other causes beyond its control (collectively referred to as the "Force Majeure") shall not be deemed to be a breach of this agreement, provided, that the party so prevented from performance of its obligations herein, shall not have caused such Force Majeure. The party so prevented shall have used reasonable diligence to avoid such Force Majeure or ameliorate its effects, and shall continue to take all actions within its power to comply as fully as possible with the terms and conditions of this agreement.

15.2	That except where the nature of the event shall prevent it from doing so, the party suffering such Force Majeure shall notify the other party in writing within seven days after the occurrence of such Force Majeure and shall in every instance, to the extent reasonable and lawful under the circumstances, use its best efforts to remove or remedy such cause with all reasonable dispatch.

15.3	That in the event of Force Majeure persists for a consecutive period of more than three months, and then the other party shall have the option to terminate the agreement without incurring any liability.

16.	TERM AND TERMINATION OF THE AGREEMENT

16.1	Unless terminated, this agreement shall remain valid for a period of 5 ( Five  ) year from date of signing this agreement.

16.2	The Company shall be entitled to terminate this agreement without any cause by giving 30 days’ notice.   

16.3	Either party may terminate this agreement by giving one month’s notice in writing to the other party without assigning any reason.  

In the event the Supplier being unable to provide the materials / products within the time frame mentioned herein or as shall be mentioned in the intimation / Purchase Order to be raised by the Company, then the Company shall have the right to forthwith terminate this agreement.  It is hereby clarified for the purpose of abundant caution that failure of the Supplier to distribute , deliver and display the products shall be considered to be a ground for termination without limiting to the terms of this Agreement that the Supplier shall be liable to pay for the damages suffered by the Company due to such non-compliance or breach of the terms and conditions of this agreement.
The grounds on which the Company can fortwith  terminate the agreement in addition to what stated hereinabove are as follows:-

a. 	The Supplier has failed to perform or discharge any of its obligations in accordance with the provisions of this Agreement, unless such event has occurred because of a Force Majeure Event, or due to reasons solely attributable to the Company without any contributory factor of the the Supplier;
b.	 if at any time any payment, assessment, charge, lien, penalty or Damage herein specified to be paid by the Supplier to the Company, or any part thereof, shall be in arrears and unpaid;
c. 	Any representation made or warranties given by the Supplier under this Agreement is found to be false or misleading;
d. 	The Supplier engaging or knowingly has allowed any of its employees to engage in any activity prohibited by law or which constitutes a breach of or an offence under any law, in the course of any activity undertaken pursuant to this Agreement;
e. 	The Supplier has been adjudged as bankrupt or become insolvent:
f. 	A resolution for voluntary winding up has been passed by the shareholders of the Supplier;
g. 	Repeated grievances had been raised by customers in respect to the quality of products within a particular period
h. 	The Supplier has failed to deliver the materials within time;
i.	The Supplier has failed to abide by the statutory regulations or there has been a gross negligence or violation of such provisions
j.	Consignment had been delivered by the Supplier which does not relate with the request placed by the Company or there had been short / excess delivery of products
k. 	The Supplier had failed to receive back the products inspite of intimation from the Company or after the stipulated period of display

Furthermore the Company shall have the exclusive right to terminate the agreement with immediate effect at any point of time during its pendency, if the Supplier fails and / or does not adhere to the following essential requisites , namely:-
i.	Quality, 
ii.	Service, 
iii.	Marketing Activities
iv.	Delay in Delivery
v.	Non acceptance of defective / damaged materials

Upon expiry of notice period of termination, both the parties shall endeavor to reconcile the accounts within 15 days from the expiry of the notice period.

17.	QUALITY POLICY	

17.1	The Company is synonymous with quality and service to its customers. Keeping the standards of quality policy of the Company, the Supplier shall adhere to the Standards prescribed under Foods Laws or any other rules, Act etc for maintaining food safety standards. The Supplier shall carry assurance of product safety and quality in accordance with prescribed standards.

17.2	If the entire product batch is defective, the Company shall have the right to immediately remove the same from display at once. In such case the cost of goods removed and the cost of logistics shall be debited on the Supplier. The Supplier has to reply back on the complaint along with counter measures taken by him within a week. The Supplier shall try to redress the complaint and reconcile with the aggrieved customer.


18.	NOTICES
Any notice or letter, required to be served by one party on another in pursuance to this Agreement shall be deemed to have been properly served on such other if delivered either by Registered Post with acknowledgement due or courier or hand delivery at the respective address mentioned here in above.

19.	AMENDMENTS & MODIFICATIONS

Any amendments or modification to the terms of this Agreement can be initiated  / intimated by either the retailer or the Vendor  by way of a letter addressed to the other party and such amendment or modification shall become binding on all the parties herein when the same is duly acknowledged and accepted by such other party.

20.	INTELLECTUAL PROPERTY RIGHTS

None of the parties shall use the Trademark, copyright or any other Intellectual property right of another in any unauthorized manner or in any advertisement, publicity whatsoever without the written permission or authorization of the owner of such Trademark, copyright or intellectual property right.

 
21.	JURISDICTION 
The courts of Kolkata will have jurisdiction to try the matter in case of any dispute arising of this agreement. 

"""

# ------------------------------------------------
# 2) HELPERS
# ------------------------------------------------
def docx_from_plain_text(plain_text: str, title: str = None) -> BytesIO:
    """Create a .docx from plain text. Adds optional centered bold title."""
    doc = Document()
    # Optional margins (nicer print layout)
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

    # Allow multi-paragraphs
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

def rephrase_clause(text: str) -> str:
    """Stub for AI rephrase. Replace with OpenAI call if desired."""
    return text

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

def build_docx(
    preamble: str,
    clause_texts: list,
    parties: list,
    annexure_note: str,
    title="AGREEMENT",
    annexure_file=None
) -> BytesIO:
    from docx.shared import Inches
    
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # Title
    add_heading(doc, title.upper(), 18, True)
    doc.add_paragraph(preamble.strip())
    doc.add_paragraph("")

    # Clauses
    for t in clause_texts:
        p = doc.add_paragraph()
        ts = t.strip()
        if len(ts) >= 2 and ts[:2].isdigit() and "." in ts[:5]:
            first_line = ts.split("\n", 1)[0]
            run = p.add_run(first_line)
            run.bold = True
            remainder = ts[len(first_line):]
            if remainder:
                doc.add_paragraph(remainder)
        else:
            p.add_run(t)
        doc.add_paragraph("")

    # Parties
    if parties:
        add_heading(doc, "PARTIES", 14, False)
        for idx, p in enumerate(parties, 1):
            doc.add_paragraph(f"{idx}. {p}")

    # Annexure note
    if annexure_note:
        doc.add_paragraph("")
        add_heading(doc, "ANNEXURE", 14, False)
        doc.add_paragraph(annexure_note)

    # Annexure table (if Excel provided)
    if annexure_file is not None:
        try:
            import pandas as pd
            df = pd.read_excel(annexure_file)

            # Page break before annexure table
            doc.add_page_break()
            add_heading(doc, "ANNEXURE – DETAILS", 14, True)

            # Create table
            table = doc.add_table(rows=1, cols=len(df.columns))
            table.style = "Table Grid"

            # Header row
            hdr_cells = table.rows[0].cells
            for j, col in enumerate(df.columns):
                hdr_cells[j].text = str(col)

            # Data rows
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
    """Return a blank Excel template for Annexure."""
    df = pd.DataFrame(
        columns=["S.No", "Item/Deliverable", "Description", "Quantity", "Unit Price", "Total", "Remarks"]
    )
    out = BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Annexure")
    out.seek(0)
    return out

def default_purchase_annexure_template() -> BytesIO:
    """Return a blank Excel template for Annexure."""
    df = pd.read_excel("Purchase_Agreement_Annexure_Fromat_Excel.xlsx")
    out = BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Annexure")
    out.seek(0)
    return out
# ------------------------------------------------
# 3) STREAMLIT APP
# ------------------------------------------------
st.set_page_config(page_title="Interactive Contract Generator", page_icon="📄", layout="wide")
st.title("📄 Interactive Contract Generator")

# GLOBAL STATE
if "workflow" not in st.session_state:
    st.session_state.workflow = "form"          # form → clauses → annexure → preview
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "clause_store" not in st.session_state:
    # {clause_no: {"text":..., "approved": False}}
    st.session_state.clause_store = {i: {"text": CLAUSES[i], "approved": False} for i in CLAUSES}
if "custom_clauses" not in st.session_state:
    st.session_state.custom_clauses = []        # list of {"title":..., "text":..., "approved": True/False}
if "parties" not in st.session_state:
    st.session_state.parties = []
if "annexure_note" not in st.session_state:
    st.session_state.annexure_note = ""
if "annexure_file" not in st.session_state:
    st.session_state.annexure_file = None

# Top selectors
entity = st.selectbox("Entity", ["", "RPSG Ventures", "PCBL", "Spencers Retail", "AquaPharm", "Nature's Basket"])
contract_type = st.selectbox(
    "Contract Type",
    ["", "NDA", "PURCHASE AGREEMENT", "Vendor Agreement", "Service Agreement", "Marketing Agreement",
     "Software License Agreement", "Supply Agreement", "Lease/Rent Agreement", "Leave and License Agreement",
     "Franchise Agreement", "Distribution Agreement", "Manufacturing Agreement", "Employment Agreement",
     "Collaboration Agreement", "MoU/LoI"],
    index=0
)

st.markdown("---")

# ================
# STEP 1: FORM UI
# ================
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
        # Keep your existing PA business inputs (18) AND add identifiers needed by PURCHASE_TEMPLATE
        pa_fields = [
            # --- Your earlier 'business' inputs (kept for clauses/annexure details) ---
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
        st.info("Select an Entity and a Contract Type to begin.")

    left, right = st.columns([1, 1])
    if left.button("Save & Go to Clauses ➡️", use_container_width=True, key="to_clauses_btn"):
        st.session_state.workflow = "clauses"
        st.rerun()
    right.button("Reset Form", on_click=lambda: st.session_state.answers.clear(), use_container_width=True, key="reset_form_btn")


# --- QUICK PREVIEW / DOWNLOAD / SUBMIT on the NDA form ---
if st.session_state.workflow == "form" and contract_type == "NDA":
    all_filled = all(st.session_state.answers.get(k, "").strip() for k in
        ["DAY","MONTH","RPSG_CIN_No","Vendor_Name","Vendor_CIN_No","Vendor_Office","RPSG_Email","Vendor_SPOC","Vendor_Email","RPSG_SPOC"]
    )

    st.markdown("### Quick actions (NDA)")
    col_q1, col_q2, col_q3 = st.columns(3)

    data = {k: st.session_state.answers.get(k, "") for k in
            ["DAY","MONTH","RPSG_CIN_No","Vendor_Name","Vendor_CIN_No","Vendor_Office","RPSG_Email","Vendor_SPOC","Vendor_Email","RPSG_SPOC"]}
    preamble = NDA_TEMPLATE.format(**data)

    approved = [st.session_state.clause_store[i]["text"]
                for i in sorted(st.session_state.clause_store)
                if st.session_state.clause_store[i]["approved"]]
    if not approved:
        approved = [st.session_state.clause_store[i]["text"] for i in sorted(st.session_state.clause_store)]

    quick_preview_text = compose_full_contract(
        preamble=preamble,
        clause_texts=approved,
        parties=st.session_state.parties,
        annexure_note=""  # NDA: no annexure
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
    st.caption("Pick a clause, edit/rephrase, then mark it Approved. Add parties or custom clauses below.")

    # colA, colB = st.columns([1, 2])
    #with colA:
    selected = st.selectbox("Standard clause (1–22)", list(CLAUSES.keys()), key="clause_select")
    display = st.session_state.clause_store[selected]["text"]

    # Rich text editor with Quill.js
    edited = st_quill(
        value=display,
        placeholder="Edit clause text here...",
        key=f"clause_quill_{selected}",
        # theme="snow",  # or "bubble"
    )

    c1, c2 = st.columns(2)
    if c1.button("Save Edit", key=f"save_edit_{selected}"):
        if edited:
            st.session_state.clause_store[selected]["text"] = edited
            st.success("Saved.")


    st.session_state.clause_store[selected]["approved"] = st.checkbox(
        "Approved",
        value=st.session_state.clause_store[selected]["approved"],
        key=f"approved_{selected}"
    )

    #with colB:
    st.write("**Parties**")
    new_party = st.text_input("Add Party (Name, Role, Address/email optional)", key="party_input")
    cpa, cpb = st.columns(2)
    if cpa.button("Add Party", key="add_party_btn"):
        if new_party.strip():
            st.session_state.parties.append(new_party.strip())
    if cpb.button("Clear Parties", key="clear_parties_btn"):
        st.session_state.parties = []
    if st.session_state.parties:
        st.write("- " + "\n- ".join(st.session_state.parties))

    st.write("**Add Custom Clause**")
    cc_title = st.text_input("Custom Clause Title", key="cc_title")
    cc_text = st.text_area("Custom Clause Text", height=160, key="cc_text")

    if st.button("Add Custom Clause", key="add_custom_clause_btn"):
        if cc_title.strip() and cc_text.strip():
            st.session_state.custom_clauses.append(
                {"title": cc_title.strip(), "text": cc_text.strip(), "approved": True}
            )
            st.success(f"Custom clause '{cc_title}' added.")
            st.rerun()   # ✅ use this instead of experimental_rerun

    # 👇 show all added custom clauses right away
    if st.session_state.custom_clauses:
        st.markdown("#### Added Custom Clauses")
        for idx, c in enumerate(st.session_state.custom_clauses, 1):
            with st.expander(f"{idx}. {c['title']}", expanded=False):
                st.write(c['text'])
                if st.button(f"❌ Remove {c['title']}", key=f"remove_cc_{idx}"):
                    st.session_state.custom_clauses.pop(idx-1)
                    st.rerun()   # ✅ updated here too




    nav1, nav2 = st.columns([1, 1])
    if nav1.button("⬅️ Back to Form", key="clauses_back_form"):
        st.session_state.workflow = "form"
        st.rerun()

    next_label = "Save & Go to Preview ➡️" if contract_type == "NDA" else "Save & Go to Annexure ➡️"
    if nav2.button(next_label, key="clauses_next_btn"):
        st.session_state.workflow = "preview" if contract_type == "NDA" else "annexure"
        st.rerun()


# =========================
# STEP 3: ANNEXURE (Excel)
# =========================
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


# =========================
# STEP 4: PREVIEW & EXPORT
# =========================
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

    store = st.session_state.clause_store

    # 👇 Toggle to control what's included
    only_approved = st.checkbox("Show only approved clauses", value=False, key="preview_only_approved")

    if only_approved:
        clause_list = [store[i]["text"] for i in sorted(store) if store[i]["approved"]]
        if not clause_list:
            st.info("No clauses approved yet; showing all clauses instead.")
            clause_list = [store[i]["text"] for i in sorted(store)]
    else:
        clause_list = [store[i]["text"] for i in sorted(store)]

    custom = [
        f"{c.get('title','Custom Clause')}\n{c.get('text','')}"
        for c in st.session_state.custom_clauses
        if c.get("approved", True)
    ]
    all_clauses = clause_list + custom

    annexure_text = "" if contract_type == "NDA" else st.session_state.annexure_note

    preview_text = compose_full_contract(
        preamble=preamble,
        clause_texts=all_clauses,
        parties=st.session_state.parties,
        annexure_note=annexure_text,
    )

    st.markdown("### 📑 Preview")
    st.markdown(preview_text.replace("\n", "<br>"), unsafe_allow_html=True)

    # 👇 Show annexure table if uploaded
    if contract_type != "NDA" and st.session_state.annexure_file:
        st.markdown("### 📎 Annexure (Preview)")
        annexure_df = pd.read_excel(st.session_state.annexure_file)
        st.dataframe(annexure_df, use_container_width=True)


    c1, c2, c3 = st.columns(3)
    with c1:
        docx_file = build_docx(
            preamble=preamble,
            clause_texts=all_clauses,
            parties=st.session_state.parties,
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
