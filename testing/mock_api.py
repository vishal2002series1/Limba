from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return "IRAH Mock API is running..."

# LEGACY - IRAH 1.0 Response
@app.post("/chat/custom-search")
def chat_custom_search():

    sample_response = {
    "additional_prompt_chunk": [
        "1d005c7c-804e-4415-96c4-624ef287d3a4,cb56cf70-dd88-4799-a1ec-109b99e5d1c1,9936af0d-6ef6-443f-8a32-ae2b8f62b157"
    ],
    "article": {
        "news_article_widget": [],
        "research_document_widget": [
            {
                "blob_file_url": "https://wamllmpocstorage.blob.core.windows.net/wam-llm-poc/research_document/J.P. Morgans North America Equity Research on Airlines.pdf?se=2026-05-03T12%3A27%3A22Z&sp=r&sv=2023-01-03&sr=b&sig=oobqXKgRcLnP1aR6kgoJnynFUjqgCscfOljsFnDgfao%3D",
                "doc_id": "J.P._Morgans_North_America_Equity_Research_on_Airlines.pdf"
            }
        ]
    },
    "company_level": {
        "company_overview": [
            {
                "founded": "December 9, 2013",
                "headquarters": "1 Skyview Drive, Fort Worth, Texas 76155, United States",
                "industry": "Passenger Airlines",
                "overview": "American Airlines Group, Inc. is a holding company, which engages in the operation of a network carrier through its principal wholly-owned mainline operating subsidiary, American. The firm offers air transportation for passengers and cargo. It operates through the following geographical segments: Department of Transportation Domestic, Department of Transportation Latin America, Department of Transportation Atlantic, and Department of Transportation Pacific.",
                "parent_organizations": "American Airlines Group, Inc.",
                "website_link": "www.aa.com"
            }
        ],
        "management_overview": [
            {
                "contact": "Phone: 1 682 278 9000",
                "employees": "129700",
                "management": "Robert D Isom Jr., MBA (Chief Executive Officer & Director),David G Seymour (Chief Operating Officer & Senior Vice President),Devon E May MBA (Chief Financial Officer & Executive Vice President),Ganesh Jayaram PhD (Executive VP, Chief Digital & Information Officer),Patricia Hollinrake (Managing Director-DCA)",
                "partnerships": "oneworld alliance,British Airways,Iberia,Finnair,Japan Airlines,Qantas Airways,LATAM Airlines Group,Expedia, Inc.,The Priceline Group,Travelocity,Orbitz,Amadeus,Sabre,Travelport,Alaska Airlines,Cape Air,Cathay Pacific,China Southern Airlines,Cathay Dragon,Etihad Airways,Fiji Airways,Hawaiian Airlines,Malaysia Airlines,Seaborne Airlines,Korean Air,Interjet,WestJet,Sri Lankan Airlines,GOL,Sonoco ThermoSafe,Boom Supersonic,Gevo, Inc.,IndiGo,Qatar Airways,Embraer,Cool Effect,JetBlue Airways"
            }
        ],
        "market_data": [
            {
                "EPS": 1.88,
                "net_income": "$1.34 B",
                "net_profit_margin": "9.52%",
                "sales": "$14.05 B",
                "stock_price": "$15.13",
                "ticker": "AAL"
            }
        ]
    },
    "metrics": {
        "tokens_used_context_": 5461
    },
    "query_id": "483387Z-4a336e7e-7fe2-4d31-aa08-ac65dcbd4891",
    "query_ques": "Who is the CFO of American Airlines?",
    "query_type": "Base Case Question",
    "req_chunk_size": 2000,
    "response_time": {
        "base_question_response_time": 7.34,
        "openai_generation_summary_response_time": 6.4,
        "question_classifier_response_time": 0.64
    },
    "source": [
        "82c70a90-b821-4604-b42c-19e96d127326,e9f7b732-364e-4b25-909e-075084efc552"
    ],
    "summarized_answer": "The CFO of American Airlines is Derek J. Kerr. He holds the position of Vice Chair, Chief Financial Officer & President-American Eagle, American Airlines Group, Inc.",
    "top_results_chunks": [
        {
            "chunks_results": [
                {
                    "chunk_id": "1d005c7c-804e-4415-96c4-624ef287d3a4",
                    "chunk_text": "American Airlines Group appoints Greg Smith as independent chairman of the board, effective 30-Apr-23 ($15.87, 0.00) Thursday, February 23, 2023 04:32:22 PM ET . Smith will succeed Doug Parker, who will retire from the board at that time. Smith's appointment is part of the board's long-term succession planning process. . Smith joined American's board in January 2022 after a more than 30-year career at The Boeing Company. He most recently served as Boeing's EVP and CFO. FACTSET | streetaccount ",
                    "chunk_token_len": "118",
                    "defined_chunk_size": "2000",
                    "doc_page_number": "1",
                    "file_word_length": "79",
                    "publication_date": "23_02_2023",
                    "recency_factor": 0.3,
                    "recency_search_score": 0.8281352757756459,
                    "score": 0.860762178898,
                    "title": ""
                },
                {
                    "chunk_id": "cb56cf70-dd88-4799-a1ec-109b99e5d1c1",
                    "chunk_text": "American Airlines Group appoints Greg Smith as independent chairman of the board, effective 30-Apr-23 ($15.87, 0.00) Thursday, February 23, 2023 04:32:22 PM ET . Smith will succeed Doug Parker, who will retire from the board at that time. Smith's appointment is part of the board's long-term succession planning process. . Smith joined American's board in January 2022 after a more than 30-year career at The Boeing Company. He most recently served as Boeing's EVP and CFO. FACTSET | streetaccount ",
                    "chunk_token_len": "118",
                    "defined_chunk_size": "2000",
                    "doc_page_number": "1",
                    "file_word_length": "79",
                    "publication_date": "23_02_2023",
                    "recency_factor": 0.3,
                    "recency_search_score": 0.8281352757756459,
                    "score": 0.860762178898,
                    "title": ""
                }
            ],
            "source_name_blob_url": [
                "Greg_Smith_Appointed_Chairman_of_American_Airlines_Group.pdf",
                "https://wamllmpocstorage.blob.core.windows.net/wam-llm-poc/wam_factset_query3/Greg Smith Appointed Chairman of American Airlines Group.pdf?se=2026-04-05T08%3A33%3A43Z&sp=r&sv=2022-11-02&sr=b&sig=Sttc2KJFOvFLzpdcx7txpncj%2BSEYcIZZuLE4QXF0Cx8%3D"
            ]
        },
        {
            "chunks_results": [
                {
                    "chunk_id": "82c70a90-b821-4604-b42c-19e96d127326",
                    "chunk_text": "Vice Chair, Chief Financial Officer & President-American Eagle, American Airlines Group, Inc. Me too. Helane Becker Analyst, Cowen & Co. LLC ... next year. Derek J. Kerr Vice Chair, Chief Financial Officer & President-American Eagle, American Airlines Group, Inc. We'll see you in Boston. Do you want to be in Boston? Robert D. Isom, Jr. Chief Executive Officer & Director, American Airlines Group, Inc. ... in Boston, is it okay? Derek J. Kerr Vice Chair, Chief Financial Officer & President-American Eagle, American Airlines Group, Inc. Too hot down here. Helane Becker Analyst, Cowen & Co. LLC I feel like it's the continual, next year in Boston. Robert D. Isom, Jr. Chief Executive Officer & Director, American Airlines Group, Inc. You know what, we're going to go to Boston no matter what next year, okay? Helane Becker Analyst, Cowen & Co. LLC [indiscernible] (00:31:38) Derek J. Kerr Vice Chair, Chief Financial Officer & President-American Eagle, American Airlines Group, Inc. So, we're coming to see you. FACTSET: callstreet 1-877-FACTSET www.callstreet.com C Corrected Transcript 07-Sep-2022 12 Copyright @ 2001-2022 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Cowen Global Transportation & Sustainable Mobility Conference C Corrected Transcript 07-Sep-2022 Helane Becker Analyst, Cowen & Co. LLC I'll meet you there. Robert D. Isom, Jr. Chief Executive Officer & Director, American Airlines Group, Inc. We've got a great operation there, too. Thanks, Helane. Helane Becker Analyst, Cowen & Co. LLC Thanks, team. Bye. Derek J. Kerr Vice Chair, Chief Financial Officer & President-American Eagle, American Airlines Group, Inc. Thank you. Helane Becker Analyst, Cowen & Co. LLC Have a great day. Derek J. Kerr Vice Chair, Chief Financial Officer & President-American Eagle, American Airlines Group, Inc. Yeah. Robert D. Isom, Jr. Chief Executive Officer & Director, American Airlines Group, Inc. Bye. FACTSET: callstreet 1-877-FACTSET www.callstreet.com 13 Copyright @ 2001-2022 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Cowen Global Transportation & Sustainable Mobility Conference Disclaimer The information herein is based on sources we believe to be reliable but is not guaranteed by us and does not purport to be a complete or error-free statement or summary of the available data. As such, we do not warrant, endorse or guarantee the completeness, accuracy, integrity, or timeliness of the information. You must evaluate, and bear all risks associated with, the use of any information provided hereunder, including any reliance on the accuracy, completeness, safety or usefulness of such information. This information is not intended to be used as the primary basis of investment decisions. It should not be construed as advice designed to meet the particular investment needs of any investor. This report is published solely for information purposes, and is not to be construed as financial or other advice or as an offer to sell or the solicitation of an offer to buy any security in any state where such an offer or solicitation would be illegal. Any information expressed herein on this date is subject to change without notice. Any opinions or assertions contained in this information do not represent the opinions or beliefs of FactSet CallStreet, LLC. FactSet CallStreet, LLC, or one or more of its employees, including the writer of this report, may have a position in any of the securities discussed herein. THE INFORMATION PROVIDED TO YOU HEREUNDER IS PROVIDED \"AS IS,\" AND TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, FactSet CallStreet, LLC AND ITS LICENSORS, BUSINESS ASSOCIATES AND SUPPLIERS DISCLAIM ALL WARRANTIES WITH RESPECT TO THE SAME, EXPRESS, IMPLIED AND STATUTORY, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, ACCURACY, COMPLETENESS, AND NON-INFRINGEMENT. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, NEITHER FACTSET CALLSTREET, LLC NOR ITS OFFICERS, MEMBERS, DIRECTORS, PARTNERS, AFFILIATES, BUSINESS ASSOCIATES, LICENSORS OR SUPPLIERS WILL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL OR PUNITIVE DAMAGES, INCLUDING WITHOUT LIMITATION DAMAGES FOR LOST PROFITS OR REVENUES, GOODWILL, WORK STOPPAGE, SECURITY BREACHES, VIRUSES, COMPUTER FAILURE OR MALFUNCTION, USE, DATA OR OTHER INTANGIBLE LOSSES OR COMMERCIAL DAMAGES, EVEN IF ANY OF SUCH PARTIES IS ADVISED OF THE POSSIBILITY OF SUCH LOSSES, ARISING UNDER OR IN CONNECTION WITH THE INFORMATION PROVIDED HEREIN OR ANY OTHER SUBJECT MATTER HEREOF. The contents and appearance of this report are Copyrighted FactSet CallStreet, LLC 2022 CallStreet and FactSet CallStreet, LLC are trademarks and service marks of FactSet CallStreet, LLC. All other trademarks mentioned are trademarks of their respective companies. All rights reserved. FACTSET: callstreet 1-877-FACTSET www.callstreet.com C Corrected Transcript 07-Sep-2022 14 Copyright @ 2001-2022 FactSet CallStreet, LLC ",
                    "chunk_token_len": "1237",
                    "defined_chunk_size": "2000",
                    "doc_page_number": "12,13,14",
                    "file_word_length": "6726",
                    "publication_date": "07_09_2022",
                    "recency_factor": 0.3,
                    "recency_search_score": 0.7874211556672128,
                    "score": 0.855428159237,
                    "title": "American Airlines Group, Inc. (AAL) Cowen Global Transportation & Sustainable Mobility Conference"
                }
            ],
            "source_name_blob_url": [
                "American_Airlines_at_Cowen_Global_Transportation_&_Sustainable_Mobility_Conference.pdf",
                "https://wamllmpocstorage.blob.core.windows.net/wam-llm-poc/wam_factset_query1/American Airlines at Cowen Global Transportation & Sustainable Mobility Conference.pdf?se=2026-04-05T06%3A13%3A25Z&sp=r&sv=2022-11-02&sr=b&sig=9ml1pyTYO9MqcwcsyIDJHzpBhVAy69auUyEpY0NO2pY%3D"
            ]
        },
        {
            "chunks_results": [
                {
                    "chunk_id": "e9f7b732-364e-4b25-909e-075084efc552",
                    "chunk_text": "So, in summary, we're grateful for the incredible work of the American Airlines team over the past year. We remain optimistic about the return of demand and we're very pleased with how American is positioned, thanks to the tremendous efforts of our team. And now with that, I'll turn it over to Derek. Derek J. Kerr Executive Vice President & Chief Financial Officer, American Airlines Group, Inc. Thanks, Robert, and good morning, everyone. Before I review the results, I would also like to thank the American Airlines team for their outstanding work during the quarter. This pandemic has been relentless. And despite the uncertainty, our team continued to show it's the best in the business. This morning, we reported a fourth quarter GAAP net loss of $931 million or a loss of $1.44 per share. Excluding net special items, we reported a net loss of $921 million or a loss of $1.42 per share. For the full-year 2021, we reported a GAAP net loss of $2 billion, and excluding net special items, we reported a net loss of $5.4 billion. Despite the impact of Omicron that we saw in this quarter, the trajectory of our revenue recovery continues to be positive, and it even exceeded our initial expectations as we outlined on our last call. Our fourth quarter revenue was down 17% compared with the same period of 2019 versus our original guidance of down 20%. This gradual improvement makes it even clearer to us that despite the uncertain demand environment, the steps we have taken over the past 24 months to bolster our network and improve our revenue-generating capabilities are working. FACTSET: callstreet 1-877-FACTSET www.callstreet.com C Corrected Transcript 20-Jan-2022 7 Copyright @ 2001-2022 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q4 2021 Earnings Call On the cost side, we remain focused on keeping our controllable costs down, and we actioned $1.3 billion in permanent annual cost initiatives in 2021, providing a new and more efficient baseline for our 2022 budget. During the fourth quarter, we made the decision to invest in the operation with a holiday pay program for our employees as well as reducing our peak holiday capacity. These actions did put pressure on our unit cost performance in the fourth quarter, but they led to a strong operational performance over that period. This included an industry-leading month of operating performance in December when it mattered the most to our customers. On the fleet side, I'm pleased to report that our fleet harmonization project is now nearly complete with our last A321 going into the shop this quarter. This is a full year ahead of our original schedule, and we're excited to have this project behind us. In addition to a consistent product and better experience for our customers, the operational benefits of having a simplified and streamlined fleet are already being realized. The changes we have made to our A321s and 737s enable us to fly 2% more total capacity than we could have with the old configuration, thus, providing a unit cost tailwind as we continue to build back our network. In addition to better unit cost, these reconfigured aircraft will also generate more revenue, allowing us to recover from the pandemic even faster. With respect to our widebody aircraft, we continue to have productive conversations with Boeing to determine the timing of our delayed 788 [787-8] deliveries that were expected to arrive last year. Due to the continued uncertainty of delivery schedule, these aircraft remain out of our near-term schedule to minimize customer disruption. We expect to fly four aircraft during our peak summer schedule. We ended the fourth quarter with $15.8 billion of total available liquidity, which is the highest year-end liquidity balance in the company's history. As we have said in the past, the deleveraging of American's balance sheet remains a top priority, and we are committed to significant debt reduction in the years ahead. Even with this volatile demand environment, we remain on track with our target of reducing overall debt levels by $15 billion by the end of 2025. In fact, as of the end of 2021, we have already reduced our overall debt levels by $3.7 billion from our peak levels in the second quarter of 2021. During the quarter, we made $706 million in scheduled debt payments, which resulted in paying off the 2013-1 EETC B tranche. In the first quarter, we expect to make $337 million of scheduled debt payments, which will include unencumbering 12 aircraft. For our pension, our funded status improved by 9.2 points to 77.9%, resulting in a $2 billion reduction in the underfunded liability on a year-over-year basis. Lastly, during the fourth quarter, we completed approximately $960 million of EETC financing, and we now have financing secured for all our 2022 deliveries through the third quarter. Our 2022 budget reflects our priorities to run a reliable airline for our customers and return to profitability. Our plan includes ongoing investments that will help build upon the positive momentum we've seen in our operations while leveraging the cost efficiencies and network enhancements we have talked so much about. We believe these actions will provide a solid baseline for both profitability and free cash flow production when demand has fully recovered. Looking to the first quarter, COVID-impacted demand and elevated fuel prices will continue to put pressure on our near-term margins. In this environment, we expect our capacity to be down approximately 8% to 10% versus the first quarter of 2019. Based on current demand assumptions and capacity plans, we expect total revenue to be FACTSET: callstreet 1-877-FACTSET www.callstreet.com C Corrected Transcript 20-Jan-2022 8 Copyright @ 2001-2022 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q4 2021 Earnings Call down approximately 20% to 22% versus the first quarter of 2019. We expect our first quarter CASM, excluding fuel and net special items, to be up between 8% and 10%. While we expect to be unprofitable on a pre-tax basis in January and February, we anticipate a material improvement and a return to profitability in March as demand returns. As for 2022 capacity, much of our plans are subject to the uncertain timing of deliveries of our 788 aircraft. As I mentioned previously, we removed these aircraft from our near-term schedule to protect our customers. This reduction is worth approximately 1 to 2 points of scheduled capacity for 2022. With this adjustment, we expect to add back our capacity throughout the year and to have full-year capacity recover to approximately 95% of 2019 levels. This, of course, is subject to the future demand environment and we always have the ability to adapt if demand conditions warrant. As we look at our costs, like other airlines, we are seeing inflationary pressures in fuel prices, hiring and training for both new hires and existing crews as we build back our operation, including on the regional side. We are also seeing increased starting wages for certain work groups, including vendors. In addition, we are seeing unit cost pressures from the rolling 788 delays as well as the impact from our ramp and mechanic contract that was ratified in early 2020. Even with these unit cost pressures, our fleet simplification strategy enables higher aircraft utilization and higher average gauge, both of which will help alleviate some of these pressures. As such, we expect our full-year CASM, excluding fuel and special items, to be up approximately 5% versus 2019, with the second half of the year much lower than the first half as we fly [ph] on (00:22:52) more efficient schedule. For the full year, our projected debt maturities are expected to be $2.6 billion. This includes the cash settlement of our $750 million unsecured notes that mature in June. Without any additional prepayment of debt, we project our total debt will be down $5.4 billion at the end of 2022 versus our peak levels in 2021. With respect to capital expenditures, we expect full-year 2022 CapEx to be approximately $2.6 billion, which is significantly lower than in previous years and versus others as our fleet replacement needs are complete. Net aircraft CapEx, including predelivery deposits, is expected to be $1.8 billion, and non-aircraft CapEx is expected to be $800 million. So, in conclusion, we are incredibly proud of our team for their continued resilience in a very challenging environment. With the bold actions we've taken and steadfast commitment of our team, we are well-positioned for the future. Now, before we open up the line to questions, I would like to acknowledge Dan Cravens for a minute. Today is Dan Cravens' 62th call, not quite as many as 107, but [ph] 67 (00:24:12) is pretty amazing, and final earnings call as part of our American Airlines, US Airways and America West team. I'd like to personally thank Dan for his two decades of service, his advocacy for both the airline and our investors and for his friendship. The continuing Dan provided - or the continuity, excuse me, Dan provided over 20 years in his role across multiple airlines, multiple crises and a global [ph] pandemic (00:24:42) is unmatched. We wish him the best of luck in his next adventure. We will be introducing [ph] Scott Long (00:24:49), who will be stepping into Dan's role from our financial planning organization later this month. So, with that, I'd like to open up the line for analyst questions. ",
                    "chunk_token_len": "1996",
                    "defined_chunk_size": "2000",
                    "doc_page_number": "7,8,9",
                    "file_word_length": "15457",
                    "publication_date": "20_01_2022",
                    "recency_factor": 0.3,
                    "recency_search_score": 0.7360319475376969,
                    "score": 0.853912472725,
                    "title": "American Airlines Group, Inc. (AAL) Q4 2021 Earnings Call"
                }
            ],
            "source_name_blob_url": [
                "American_Airlines_Q4_2021_Earnings_Call.pdf",
                "https://wamllmpocstorage.blob.core.windows.net/wam-llm-poc/wam_factset_query1/American Airlines Q4 2021 Earnings Call.pdf?se=2026-04-05T06%3A17%3A11Z&sp=r&sv=2022-11-02&sr=b&sig=lCmjm6VeddC%2BYoMoMN%2BIlQ2Oh1U7qkKq/ygplfLMCPI%3D"
            ]
        },
        {
            "chunks_results": [
                {
                    "chunk_id": "9936af0d-6ef6-443f-8a32-ae2b8f62b157",
                    "chunk_text": "Chief Revenue Officer, American Airlines Group, Inc. Yeah. William Douglas Parker A Chairman & Chief Executive Officer, American Airlines Group, Inc. Thank you, Mike. Michael Linenberg Q Analyst, Deutsche Bank Securities, Inc. Thanks. 15 FACTSET: callstreet 1-877-FACTSET www.callstreet.com Copyright @ 2001-2020 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q2 2020 Earnings Call C Corrected Transcript 23-Jul-2020 Operator: Thank you. Our next question comes from the line of Jamie Baker with JPMorgan. Your line is now open. Jamie N. Baker Q Analyst, JPMorgan Securities LLC Hey. Good morning, everybody. I guess, this means I'll wrap up the cactus triumvirate, given that Helane and Mike have already opined. Derek, can you walk through how the brand and the website is worth enough to support up to $5 billion of additional first-lien debt when loyalty is already pledged elsewhere? I mean, those are pretty material figures and we don't think that most investors had those in their liquidity models prior to today's disclosures. Derek J. Kerr Executive Vice President & Chief Financial Officer, American Airlines Group, Inc. A Right. No. I mean, we have an appraisal on both of the transactions. I mean, as we went into this process, as you know, we ran appraisals on everything because we needed to do that as we were looking at the government loan and what we wanted to do with the government loan. So, we ran an appraisal just on the frequent flyer program, and then we separated out everything else and put it into the brand discussion, I would say. The value of that is, it depends on where the value is, but somewhere in the $10 billion range, whereas the frequent flyer program, as we've announced before, is somewhere in the $20 billion range. So, we've done appraisals on both. The transaction we've been working on for a little bit, this recent one, and as we negotiated, got ourselves the ability to do an extra $4 billion underneath that transaction and it's held up by an appraisal that we've done. Jamie N. Baker Analyst, JPMorgan Securities LLC Q And in regards to a potential forward mileage sale, are you - have you reached a conclusion with Treasury yet that you could speak to that potential phenomenon? Derek J. Kerr Executive Vice President & Chief Financial Officer, American Airlines Group, Inc. A We have not reached a conclusion with Treasury yet. We're still working with Treasury on the $4.75 billion transaction and where we will go there. But I think as we've seen, if it is not a forward miles transaction on top of that, as you know, our competitor was very successful and did a really nice transaction to take their frequent flyer program and take it to the market, that is available. It probably would take us a little bit of time to do that just because our company is - our frequent flyer program is not set up as a separate company, which our competitor's was for them the ability to do that transaction. So, that ability is there. We were at $4.75 billion. We have a bigger program. And I think they raised $6.8 billion, $6.9 billion against it. So, I think, in the future, that transaction is there. It's not there today for us. But it is there in the future. So, if we can utilize the room underneath the government loan, that transaction is available in the future. Jamie N. Baker Analyst, JPMorgan Securities LLC Q And if I can just squeeze a short third one in. On JetBlue, can you just remind us what you can and can't do in regards to the partnership? What level of coordination, pricing, scheduling is legally permissible? Vasu Raja A Chief Revenue Officer, American Airlines Group, Inc. FACTSET: callstreet 1-877-FACTSET www.callstreet.com 16 Copyright @ 2001-2020 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q2 2020 Earnings Call C Corrected Transcript 23-Jul-2020 Yeah. I can. Thanks for the question, Jamie. Look, the way we've envisioned it, it would be really a pretty broad partnership where, of course, we would have extensive code sharing back and forth, frequent flyer benefits, and a big amount of corporate dealing. A big part of what makes this go, certainly, as we look at it, is something that we think will be great for customers, for our team, too. We envision being able to take out things like 50-seat regional jets, which are, in many ways, really uncompetitive product in a place like New York or Boston; and arrange a number of slot moves within JFK and LaGuardia such that certainly AA can grow its mainline presence. That's where you see us adding more long-haul services in New York and indeed, over time, we anticipate being able to do a whole lot more of that. And then, of course, also for our new partner, JetBlue, they also get to go and expand. So, in doing that, we see a lot of ways that we can get work together that may be a little unconventional from traditional code shares in the past, but can create a huge benefit for our customers, a very big benefit to our team and can help both of these airlines really participate in the recovery as and when it happens. Jamie N. Baker Q Analyst, JPMorgan Securities LLC Thanks, gentlemen. William Douglas Parker A Chairman & Chief Executive Officer, American Airlines Group, Inc. Thanks, Jamie. Operator: Thank you. Our next question comes from the line of Dan Mckenzie with Seaport Global. Your line is now open. Dan J. Mckenzie Q Analyst, Seaport Global Oh. Hey. Thanks. Good morning, guys. William Douglas Parker A Chairman & Chief Executive Officer, American Airlines Group, Inc. Hey. Dan J. Mckenzie Q Analyst, Seaport Global Just following up on that - the alliance with JetBlue and Alaska, I guess, if I heard correctly, it's 23% of the flying in 2019. Is the goal to get that back to industry parity was or do you think you can get - with these alliances, get to a premium? And I guess, kind of where I'm going is for investors, as they think about 23% of the flying, is this revenues that could improve 10% across 23% the flying if we get back to parity? Vasu Raja A Chief Revenue Officer, American Airlines Group, Inc. Yeah, that's an excellent question, Dan, and a sound way to think of the problem. Yes, look - and to clarify the numbers, in 2019, about 22%, 23% of our capacity base was on the West Coast: New York, Boston, right, compare that to our two strongest performing markets of DFW and Charlotte, which collectively represented about FACTSET: callstreet 1-877-FACTSET www.callstreet.com 17 Copyright @ 2001-2020 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q2 2020 Earnings Call C Corrected Transcript 23-Jul-2020 48%, 49% of the airline. So, there's a material amount of capacity that was - and for a long time has been producing RASMs below the industry average. Now, in the perfect back half of 2019, I think a lot of the way you described that makes sense. The open question is how the world recovers, how quickly we can achieve steady state. But for that reason, these partnerships are all the more critical to be able to be done now because the reality is left to everyone's own devices, the third and fourth largest carriers in New York just won't be able to compete for a diminished New York originating premium customer given the current demand outlook that's there. So, by having this, maybe a little bit of time before we're able to achieve some of the financial goals that we want from this thing. But, for us, as long as we are doing what is right by the customer in New York and Boston providing real competition to the larger networks that we face there, there's a real path for how we go about doing it. And as you say, there's probably a lot of upside. There's this thing that we envision being able to go and certainly scale the massive fixed expenses of operating in a place like New York over things like wide-bodies instead of over things like 50-seat regional jets. So, we think that there's a lot of long-term economic benefit there. The current crisis that the pandemic creates, the uncertainty in demand makes it a little bit of an uncertain path for how we go from here to there. But the core way in which you're thinking about it is similar to how we think about it. Dan J. Mckenzie Analyst, Seaport Global Q Very good. I guess, a follow-up question here, Doug, going back to your commentary this morning on CNBC to generate cash next year and start paying down debt, or maybe this is for Derek, based on what you see today and what's in the business plan, can you give us a balance sheet roadmap from here? What's the range of debt you would aspirationally or could prepay next year? And what do you want the balance sheet to look like realistically at the end of the next year, and then, as we look three years down the road? William Douglas Parker ",
                    "chunk_token_len": "1992",
                    "defined_chunk_size": "2000",
                    "doc_page_number": "15,16,17,18",
                    "file_word_length": "15127",
                    "publication_date": "23_07_2020",
                    "recency_factor": 0.3,
                    "recency_search_score": 0.6199326895781824,
                    "score": 0.858734726906,
                    "title": "American Airlines Group, Inc. (AAL) Q2 2020 Earnings Call"
                }
            ],
            "source_name_blob_url": [
                "American_Airlines_Q2_2020_Earnings_Call_Transcript.pdf",
                "https://wamllmpocstorage.blob.core.windows.net/wam-llm-poc/wam_factset_query1/American Airlines Q2 2020 Earnings Call Transcript.pdf?se=2026-04-05T06%3A17%3A08Z&sp=r&sv=2022-11-02&sr=b&sig=iFMe4nnHqlKt3yoY96q3DilbXAsoIEveOGEDGofEzyg%3D"
            ]
        }
    ]
}

    return sample_response

# NEW - IRAH 2.0 Response
@app.post("/irah/chat")
def irah_chat():

    sample_response_content = {
        "question": "Who is the CFO of American Airlines?",
        "response": "The CFO of American Airlines is Derek J. Kerr.",
        "annotations": {
            "ContentSearchTool": {
                "content_used": [
                    "79e9ec4f-1652-4080-af5a-ef7c3a22682a"
                ],
                "content_retrieved": [
                    [
                        {
                            "page_content": "F 20-Jan-2022 American Airlines Group, Inc. (AAL) Q4 2021 Earnings Call FACTSET: callstreet 1-877-FACTSET www.callstreet.com Formatted Report Total Pages: 27 Copyright @ 2001-2022 FactSet CallStreet, LLC F American Airlines Group, Inc. (AAL) Q4 2021 Earnings Call CORPORATE PARTICIPANTS \n<table-start> \n\n Daniel E. Cravens,Derek J. Kerr\nManaging Director-Investor Relations,Executive Vice President & Chief Financial Officer\nWilliam Douglas Parker,Vasu Raja\nChairman & Chief Executive Officer,Chief Commercial Officer\nRobert D. Isom,Maya Leibman\nPresident,Executive Vice President and Chief Information Officer\nOTHER PARTICIPANTS,\nJamie N. Baker,Andrew G. Didora\nJPMorgan Securities LLC,BofA Securities, Inc.\nMichael Linenberg,Alison Sider\nDeutsche Bank Securities, Inc.,The Wall Street Journal\nHelane Becker,David Koenig\nCowen and Company LLC,The Associated Press\nDuane Pfennigwerth,Mary Schlangenstein\nEvercore Group LLC,Bloomberg News\nHunter Keay,Leslie Josephs\nWolfe Research LLC,CNBC\nDavid Vernon,David Slotnick\nSanford C. Bernstein & Co. LLC,The Points Guy\nDaniel Mckenzie,Dawn Gilbertson\nSeaport Global Securities LLC,USA TODAY\nCatherine O'Brien,\nGoldman Sachs & Co. LLC, \n\n <table-end>\n FACTSET: callstreet 1-877-FACTSET www.callstreet.com Formatted Report 20-Jan-2022 2 Copyright @ 2001-2022 FactSet CallStreet, LLC F American Airlines Group, Inc. (AAL) Q4 2021 Earnings Call MANAGEMENT DISCUSSION SECTION Daniel E. Cravens Managing Director-Investor Relations GAAP AND NON-GAAP FINANCIAL MEASURES . In addition, we will be discussing certain non-GAAP financial measures this morning, which excluded the impact of unusual items . A reconciliation of those numbers to the GAAP measures is included in the earnings release and that can be found in the Investor Relations section of our website William Douglas Parker Chairman & Chief Executive Officer BUSINESS HIGHLIGHTS Opening Remarks . We have a lot to cover today, but I'm going to start with the big news since last quarter's call, at least for me, which is that Robert Isom is going to be the next CEO of American Airlines · That change is effective on March 31st . I'm going to remain Chairman of the American Board, but importantly, I will have no executive duties · Robert will be fully in charge . I will stand as Chairman for as long as Robert and the board find that a value . This is terrific news for our team . Robert is going to be the ninth CEO in the nearly 100-year history of American Airlines, which we believe is the best job in all of aviation . And we all are excited for Robert and for American · As you all know, Robert's someone I've worked alongside for several decades o He's an extraordinary team builder, who understands the complexities of operating an airline like American o He loves the people of American, and he brings a fresh perspective to the future of American :unselected: o I know he's going to accomplish great things, and I'm looking forward to watching that happen along with all of you Transition . Now, what this transition does mean is this is going to be my last earnings call with you all, which is kind of a big deal for me . I've had a speaking role on every quarterly earnings call since I became CFO of America West Airlines in June of 1995 . So, by my calculations, this makes this my 107th consecutive quarterly call FACTSET: callstreet 1-877-FACTSET www.callstreet.com Formatted Report 20-Jan-2022 3 Copyright @ 2001-2022 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q4 2021 Earnings Call . So, look, I'm going to try not to speak as much on this one as I have on the first 106 calls, especially as it relates to the company's go-forward plans, rather, I'm going to let those who are leading American into the future to talk about that future Appreciation . But before I turn over the stage, I do have a couple of quick thank yous . First is to you all, the sell-side analysts and the reporters, who cover our business ",
                            "content_id": "412411aa-e63a-4edc-bbe5-375c4a721405",
                            "doc_name": "AAL Q4 2021 Earnings Call Summary.pdf",
                            "content_doc_pages": [
                                1,
                                2,
                                3,
                                4
                            ],
                            "content_tokens": 977,
                            "doc_words": 13816,
                            "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q4%202021%20Earnings%20Call%20Summary.pdf",
                            "doc_path": "irah-storage-2/testing/wealth",
                            "doc_details": {
                                "publication_date": "20_01_2022",
                                "company_name": "American Airlines Group, Inc. (AAL)",
                                "industry_name": "Aviation"
                            },
                            "doc_id": "985754Z-1dcd7b13-29ba-4506-a42b-b84779f6e50c",
                            "doc_tags": [
                                "wealth"
                            ]
                        },
                        {
                            "page_content": "Fortunately, with this latest issue with the MAX, we haven't had to make too many changes, but I'd just like to underscore this. Boeing has been a great partner, Airbus is a great partner. But look, at the end of the day, we need them to be incredibly reliable. We need them to be better than what they've been. And I communicate very frequently with the Boeing senior management team, and we need them to get their act together. We need a very, very strong Boeing, and we need them to be an incredible partner, and we have all the confidence that they'll get there. Devon, did you want to add anything else in terms of the particulars? Devon E. May Chief Financial Officer Just a reminder, we have four 787 deliveries this year, we took one in Q1. We expect the next three in the next 30 days or so. And on the MAXs, we have 17 remaining. Those will start to deliver over the next handful of weeks. The last two deliveries for this year are both Neos and we got both of those in Q1. Alison Sider The Wall Street Journal Thanks. And if I could just follow up on sort of all the business travel talk on this call, you've talked about it a lot, but - we have heard companies and agencies sort of complaining about some of the changes American has made. Are you seeing any market share shift? Or is it that it just doesn't really matter in the same way it might have at one point? Vasu Raja Chief Commercial Officer Hey, Ali, this is Vasu. Thanks for the question. Look, from a given agency or another, we may see a little bit. But in aggregate, we're really encouraged by the revenue trends that we see. Indeed, what we're seeing and while probably many people in traditional travel distribution are adjusting to these changes, but we also see in other cases, end consumers really responding favorably. So I mentioned earlier how many of our sales are going direct. But one of the things that we're encouraged by is by the end of this month, over 60% of our servicing transactions are coming digitally. And we anticipate by the end of the year, 100% of our transactions could be done digitally. And so that's a really meaningful change. So again, when you think about who those customers are that are increasingly traveling, whether they're traveling on a blended trip or a business trip or a leisure trip, is kind of a second-order issue. The more that we can give them a contemporary retailing experience, like what they get with anything else they buy, the more they value. We're seeing that over and over again. Our best channel for driving upsell is actually dotcom and the app. And it's consistent across our system. I'll give a for-example. This will be relevant for you even for Jamie's comment. It's not just a function of our domestic marketplace. But when we're seeing 10 to 15 points of transaction share shift out of travel agencies and into the direct channel, it applies in our long-haul network too. So London Heathrow, which for us has - our peak flights in London Heathrow, the entirety of the premium cabin could have been sold outside of the dotcom at one point in time in the past. As we finish Q1 here, about 40% of our sales in London Heathrow premium cabin is coming through our direct channel. And so much of what's happening when they're doing that is - when customers are buying that is they're buying a product that they can go service themselves, they can change their seat assignment. They get the full value of not just the flexibility of the fare product but the entirety of the servicing experience. So actually, so many of our changes that we want to make that same thing available to all of our retail outlets. Wherever a customer wants to shop, we want them to be able to have that experience as well. And we know that FACTSET: callstreet 1-877-FACTSET www.callstreet.com F Formatted Report 27-Apr-2023 A Q A 20 Copyright @ 2001-2023 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q1 2023 Earnings Call many of our travel agency partners and our corporates want the exact same thing, but it calls for a different approach. And so we are doing a little bit of innovation to go and get it to a different approach, but ultimately it's something which benefits the end customer and it's going to create more choices for them and, frankly, more competition on how they buy travel. Mary Schlangenstein Bloomberg Hey, good morning. Hey, I wanted to ask what are American's plans for taking advantage of the waivers that were offered in New York and DC by the FAA? ",
                            "content_id": "6cc91c02-47be-4afb-b8d6-7a77b8c04fd3",
                            "doc_name": "AAL Q1 2023 Earnings Call Summary.pdf",
                            "content_doc_pages": [
                                20,
                                21
                            ],
                            "content_tokens": 993,
                            "doc_words": 12732,
                            "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q1%202023%20Earnings%20Call%20Summary.pdf",
                            "doc_path": "irah-storage-2/testing/wealth",
                            "doc_details": {
                                "publication_date": "27_04_2023",
                                "company_name": "American Airlines Group, Inc. (AAL)",
                                "industry_name": "Airline"
                            },
                            "doc_id": "813067Z-be57ada5-ae35-4a56-89b8-7f3b1dffe5d9",
                            "doc_tags": [
                                "wealth"
                            ]
                        },
                        {
                            "page_content": "Copyright @ 2001-2021 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q4 2020 Earnings Call that it's early, but is there a read on what it's going to take for these - for countries to get a little more comfortable with this idea, maybe [ph] COVID (00:43:25) metrics, or what might they want to see? Alison Taylor Chief Customer Officer Yeah. Luckily, we've got great partners, we don't do this alone. So, working with tourism bodies or our hotel partners, we have been able to stand up very quickly in 90-plus markets testing. And of course, we have our VeriFLY health wallet that provides all the documentation to say, yes, you're ready to travel; you've got to check here, you can go. And actually, as an example, Dan, on Tuesday, we had 1,000-plus travelers coming back from Cancun to the US, everyone checked in and boarded successfully and had their negative test. So, we've been able to facilitate this through communication with our customers and being very proactive with our notifications and calling customers directly and working on the ground across every station led by Jose Freig, who's done a great job making sure that on the ground we're ready to help our customers. Jamie N. Baker JPMorgan Securities LLC Q Very thorough call. Most of my questions have been answered. But Derek, you've disclosed ... William Douglas Parker Chairman & Chief Executive Officer Seriously? Derek J. Kerr Executive Vice President and Chief Financial Officer .being able to achieve 2019 capacity on 10% fewer aircraft. Would you be able to express the capacity base that would be required to get you back to 2019 ex-fuel CASM? Apologies if I missed that in your prepared remarks? Derek J. Kerr Executive Vice President and Chief Financial Officer Capacity base, meaning number of aircraft? Jamie N. Baker JPMorgan Securities LLC No, ASMs. And if 2019 is even the correct base to be using? That's just sort of become the industry standard at the moment. How much capacity do you have to operate to get back to 2019? Derek J. Kerr Executive Vice President and Chief Financial Officer No, all we're trying to do is - I mean, obviously, we're not back to those levels yet, and we don't know when we're going to be back to those levels. All we're trying to do is acquaint to the fact that if we did get back to 2019 levels, we could do it with a significant amount fewer aircraft because we got - we don't have to add a bunch of aircraft to get to those levels. FACTSET: callstreet 1-877-FACTSET www.callstreet.com F Formatted Report 28-Jan-2021 A A A A A 18 Copyright @ 2001-2021 FactSet CallStreet, LLC American Airlines Group, Inc. (AAL) Q4 2020 Earnings Call Our spares are down. Our maintenance allocations are down. The MAX has come back, which were down in 2019. So, we have a significant amount of utilization increase and gauge increase in our fleet, so that we would not have - in order for us to get to 2019 levels, the point is that we would not need anywhere near as many aircraft to get to those levels ... Jamie N. Baker JPMorgan Securities LLC Right. Derek J. Kerr Executive Vice President and Chief Financial Officer .because of those things. [indiscernible] (00:45:58) Whether that's the right point, it's just - it's a level that we know and that we were at back at that point in time. Hopefully, some day in the future, we'll be ahead of those levels. Jamie N. Baker JPMorgan Securities LLC Q Sure. Would you have a corresponding ex-fuel CASM number that would then equate to the 2019 capacity? So [indiscernible] (00:46:17) ... Derek J. Kerr Executive Vice President and Chief Financial Officer No, we do not have ... Jamie N. Baker JPMorgan Securities LLC Okay. All right. Derek J. Kerr A Executive Vice President and Chief Financial Officer No, we don't have that right now. Yeah. Jamie N. Baker JPMorgan Securities LLC Q :selected: And second, I came into the call - Mark and I also curious on what the net proceeds of PSP were going to be, and I think you answered this in response to Savi's question. So, is the $300mm in incremental labor the only thing we net out or were there any other additional operating costs? Derek J. Kerr Executive Vice President and Chief Financial Officer That's what you would net out. Helane Becker Cowen and Company, LLC ",
                            "content_id": "79e9ec4f-1652-4080-af5a-ef7c3a22682a",
                            "doc_name": "AAL Q4 2020 Earnings Call Summary.pdf",
                            "content_doc_pages": [
                                17,
                                18,
                                19
                            ],
                            "content_tokens": 992,
                            "doc_words": 12840,
                            "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q4%202020%20Earnings%20Call%20Summary.pdf",
                            "doc_path": "irah-storage-2/testing/wealth",
                            "doc_details": {
                                "publication_date": "NA",
                                "company_name": "American Airlines Group, Inc. (AAL)",
                                "industry_name": "Airline"
                            },
                            "doc_id": "939486Z-d7304eee-3107-40a6-94a0-6aecc3e8c0be",
                            "doc_tags": [
                                "wealth"
                            ]
                        }
                    ]
                ]
            }
        },
        "tools": {
            "ContentSearchTool": {
                "search_type": "hybrid",
                "content_retrieved": 3
            },
            "DatabaseSearchTool": {},
            "FinancialPlannerTool": {}
        },
        "system_metrics": {
            "llm_usage_metrics": {
                "total_tokens": 5137,
                "prompt_tokens": 4952,
                "completion_tokens": 185,
                "total_cost": 0.15966,
                "successful_requests": 2,
                "llm_model_name": "gpt-4-1106-preview",
                "temperature": 0.0
            },
            "agent_reasoning_steps": [
                "tool='ContentSearchTool' tool_input='Who is the current CFO of American Airlines?' log='To find out the current CFO of American Airlines, I would need to search for the latest available information, which could be found in financial reports, news articles, or corporate announcements.\\n\\nAction: ContentSearchTool\\nAction Input: Who is the current CFO of American Airlines?'"
            ],
            "agent_response_time": 24.0
        }
    }
    sample_response_data = {
        "question": "Can you lookup the meeting notes from last interaction with Paul Benson?",
        "response": "The meeting notes from the last interaction with Paul Benson are: \"Client was due for annual review of their financial plan & goals. Client recently had a child Grace this year. Client has already added her as a beneficiary to his profile. Client had opened a 529 account online for Grace's college savings. Discussed investment strategies with a more...\"",
        "annotations": {
            "DatabaseSearchTool": {
                "sql_query": [
                    "SELECT meeting_notes FROM client_notes WHERE client_name = 'Paul Benson' ORDER BY date_of_meeting DESC LIMIT 1",
                    ""
                ]
            }
        },
        "tools": {
            "ContentSearchTool": {
                "search_type": "hybrid",
                "content_retrieved": 3
            },
            "DatabaseSearchTool": {},
            "FinancialPlannerTool": {}
        },
        "system_metrics": {
            "llm_usage_metrics": {
                "total_tokens": 12408,
                "prompt_tokens": 11957,
                "completion_tokens": 451,
                "total_cost": 0.38576999999999995,
                "successful_requests": 7,
                "llm_model_name": "gpt-4-1106-preview",
                "temperature": 0.0
            },
            "agent_reasoning_steps": [
                "(AgentAction(tool='DatabaseSearchTool', tool_input='What are the meeting notes from the last interaction with Paul Benson?', log='To find the meeting notes from the last interaction with Paul Benson, I will need to search the client relationship data.\\n\\nAction: DatabaseSearchTool\\nAction Input: What are the meeting notes from the last interaction with Paul Benson?'), {'input': 'What are the meeting notes from the last interaction with Paul Benson?', 'tables': [{'table_name': 'cash_transfer_data', 'table_description': \"The 'cash_transfer_data' table contains information about cash transfers within a firm's funds. It includes a unique 'batch_id' as the primary key, details about the portfolio manager, the firm, and the fund involved in the cash transfer. The table also tracks the date when the cash transfer was requested ('date_requested') and the date of the batch ('batch_date'). Financial figures such as 'start_of_day_cash', 'intraday_cash_transfers', 'accrued_interest', 'proforma', 'proforma_plus', and 'work_in_progress_orders' are recorded, along with an indication of whether the transaction was a 'buy' or 'sell'.\"}, {'table_name': 'client_data', 'table_description': 'The client_data table contains personal and financial information about clients. It includes fields for client identification, personal details (such as name, date of birth, age, marital status, dependents, etc.), contact information, employment and income details, client relationship information (such as client since, last login, preferred contact method, etc.), asset details (such as total assets, managed assets, retirement assets, etc.), account information, and investment preferences. The primary key of the table is client_id.'}, {'table_name': 'client_notes', 'table_description': \"The 'client_notes' table contains records of notes taken during meetings between advisors and their clients. It includes the client's ID and name, the advisor's ID and name, the date of the meeting, the category of the meeting, and the detailed notes from the meeting. The 'client_id' and 'advisor_id' fields are likely to be foreign keys that reference other tables containing client and advisor details, respectively. The 'category' field indicates the type of meeting, such as 'Annual Financial Planning / Review' or 'Mortgage Refinancing Strategy'. The 'meeting_notes' field contains extensive text detailing the discussion points and outcomes of the meetings.\"}, {'table_name': 'client_status', 'table_description': \"The client_status table contains information about the status of clients' accounts. It includes fields such as client_id, client_name, advisor_id, advisor_name, client_type, client_onboarding_status, client_pending_onboarding_activities, account_type, account_status, date_of_request, account_opening_stage, funding_stage, amount_funded, current_responsible_department, current_owner, and reason_for_account_closure. This table is used to track the onboarding process of clients, the status of their accounts, and any pending activities related to account opening or funding.\"}, {'table_name': 'net_cash_flows', 'table_description': 'The net_cash_flows table contains records of cash inflows and outflows for various funds. Each record includes a unique transaction_id, the name of the fund (fund_name), the type of partnership (partnership_type), the date of the transaction (transaction_date), the type of cash flow (cash_inflow_or_outflow), and the amount of the cash flow in dollars (cash_flow_contribution_amount_dollars). The transaction_id serves as the primary key for the table.'}, {'table_name': 'portfolio_construction', 'table_description': \"The 'portfolio_construction' table contains information about various holdings within a fund's portfolio. It includes fields such as the FIGI identifier, holding name, fund name, whether it's a fixed income security, percentage of net assets, maturity date, coupon rate, asset class, market value, par value of contracts, and the broker involved. The primary key is the 'identifier_figi' which is a unique identifier for each holding.\"}, {'table_name': 'primary_benchmark', 'table_description': 'This table contains information about benchmarks used for comparison against portfolios. It includes a unique identifier for each benchmark (benchmark_id), whether it is a primary benchmark or part of a portfolio (primary_benchmark_or_portfolio), the market capitalization category (small_cap_mid_cap_or_large_cap_fund), the investment strategy (investment_strategy), and the percentage of assets allocated along with weight allocation (percentage_of_assets_allocated_and_weight_allocation). The primary key of the table is benchmark_id.'}, {'table_name': 'security_ratings_data', 'table_description': 'The `security_ratings_data` table contains information about security ratings for various companies. It includes a unique identifier for each rating (`rating_id`), the date of the rating (`rating_date`), whether there was a change in the rating (`rating_change`), the direction of the rating change (`rating_increase_or_decrease`), the name of the company being rated (`company_name`), the ticker symbol of the company (`ticker`), the fund associated with the rating (`fund`), the rating itself (`rating`), and the source of the rating (`source`). The primary key of the table is `rating_id`.'}, {'table_name': 'trade_blotter', 'table_description': 'A record of trade transactions including fields for trade identification, trade and settlement dates, currency, broker identifiers, security information, trade execution details, and fulfillment duration.'}], 'output': 'The meeting notes from the last interaction with Paul Benson are: \"Client was due for annual review of their financial plan & goals. Client recently had a child Grace this year. Client has already added her as a beneficiary to his profile. Client had opened a 529 account online for Grace\\'s college savings. Discussed investment strategies with a more...\"', 'intermediate_steps': [(AgentAction(tool='GetColumnInfo', tool_input='client_notes', log='Thought: To find the meeting notes from the last interaction with Paul Benson, I need to identify the table that contains meeting notes and client names.\\n\\nAction: GetColumnInfo\\nAction Input: client_notes'), [{'table_name': 'client_notes', 'columns': [{'column': 'client_id', 'column_description': 'The unique identifier for the client.', 'column_metadata': 'VARCHAR(1000)', 'column_sample_data': 'C01234'}, {'column': 'client_name', 'column_description': 'The name of the client.', 'column_metadata': 'VARCHAR(1000)', 'column_sample_data': 'Derek Vang'}, {'column': 'advisor_id', 'column_description': 'The unique identifier for the advisor.', 'column_metadata': 'VARCHAR(1000)', 'column_sample_data': 'A01567'}, {'column': 'advisor_name', 'column_description': 'The name of the advisor.', 'column_metadata': 'VARCHAR(1000)', 'column_sample_data': 'Wendy Hyde'}, {'column': 'date_of_meeting', 'column_description': 'The date when the meeting took place.', 'column_metadata': 'DATE', 'column_sample_data': '2023-03-26'}, {'column': 'category', 'column_description': 'The category of the meeting.', 'column_metadata': 'VARCHAR(1000)', 'column_sample_data': 'Annual Financial Planning / Review'}, {'column': 'meeting_notes', 'column_description': 'The notes taken during the meeting.', 'column_metadata': 'VARCHAR(25000)', 'column_sample_data': 'Client was due for annual review of their financial plan & goals.'}]}]), (AgentAction(tool='sql_db_query_checker', tool_input=\"SELECT meeting_notes FROM client_notes WHERE client_name = 'Paul Benson' ORDER BY date_of_meeting DESC LIMIT 1;\", log=\"The 'client_notes' table contains the information I need, specifically the 'client_name' and 'meeting_notes' columns. I will use these columns to find the meeting notes from the last interaction with Paul Benson.\\n\\nAction: sql_db_query_checker\\nAction Input: SELECT meeting_notes FROM client_notes WHERE client_name = 'Paul Benson' ORDER BY date_of_meeting DESC LIMIT 1;\"), \"SQL Query:\\n\\n```sql\\nSELECT meeting_notes FROM client_notes WHERE client_name = 'Paul Benson' ORDER BY date_of_meeting DESC LIMIT 1;\\n```\"), (AgentAction(tool='sql_db_query', tool_input=\"SELECT meeting_notes FROM client_notes WHERE client_name = 'Paul Benson' ORDER BY date_of_meeting DESC LIMIT 1;\", log=\"The query has been checked and is ready to be executed to find the meeting notes from the last interaction with Paul Benson.\\n\\nAction: sql_db_query\\nAction Input: SELECT meeting_notes FROM client_notes WHERE client_name = 'Paul Benson' ORDER BY date_of_meeting DESC LIMIT 1;\"), \"[('Client was due for annual review of their financial plan & goals.\\\\n•\\\\tClient recently had a child Grace this year. Client has already added her as a beneficiary to his profile\\\\n•\\\\tClient had opened a 529 account online for Graces college savings. Discussed investment strategies with a more...',)]\")]})"
            ],
            "agent_response_time": 135.0
        }
    }
    return sample_response_content

#  To run the Mock API app, run the command below:
#  uvicorn mock_api:app --reload --port=5000