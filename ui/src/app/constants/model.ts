import { SafeHtml } from "@angular/platform-browser";

export interface UserProfile {
    access_token: string,
    expires_on: string,
    id_token: string,
    provider_name: string,
    user_claims: {
        typ: string,
        value: string
    }[];
    user_id: string
}[]

export interface ChatResponse {
    type: string;
    query?: string;
    response?: ContentResponse;
}[];

export interface ContentResponse {
    question: string; 
    response: string;
    marked_response: SafeHtml; 
    copy_response: string;  
    annotations: {
        ContentSearchTool: {
            content_used: ContentRetrieved[],
            other_relevant_content: ContentRetrieved[]
        },
        DatabaseSearchTool?: {
            sql_query?: string[]
        },
        GoogleSearchTool: {
            urls_used: ContentRetrieved[],
            other_relevant_urls: ContentRetrieved[]
        },
        solution_plan?: string,
        reasoning_steps?: string
    },
    tools?: {
        ContentSearch?: {
            search_type?: string,
            content_retrieved?: number
        },
        DatabaseSearch?: {}
    }
    financialContent: FinancialContent[];
    status?: string,
    // error_message? : string,
    message?: string,
    query_type?: string,

    content: ContentRetrieved[];
    contentUsed: ContentRetrieved[];

}

export interface ContentRetrieved {
    url: string,
    title: string,
    contents: string,

    page_content: string,
    marked_page_content: SafeHtml,
    sliced_page_content: SafeHtml,
    content_id: string,
    doc_name: string,
    content_doc_pages: number[],
    content_tokens: number,
    doc_words: number,
    doc_url: string,
    doc_path: string,
    doc_details: {
        publication_date: string,
        company_name: string,
        industry_name: string
    },
    doc_id: string,
    doc_tags: string[]
    showMore?: boolean,
    made_url?: string
}

export interface Client {
    client_data: {
      name: string;
      age: number;
      retirement_age: number;
      total_savings: number;
      monthly_income: number;
      deposit_rate: number;
      location: {
        city: string;
        state: string;
      };
      retirement_accounts: {
        type: string;
        balance: number;
        contribution: number;
        annual_growth: number;
      }[];
      trust_fund_accounts: {
        beneficiary: string;
        balance: number;
        contribution: number;
        annual_growth: number;
      }[];
      house: {
        value: number;
        mortgage_balance: number;
        monthly_payment: number;
        interest_rate: number;
        years_left: number;
      };
      other_investments: {
        type: string;
        balance: number;
        annual_growth: number;
      }[];
    };
}
    
export interface FinancialContent {
  financialType: string;
  financialString: string;
  markedString?: SafeHtml;
}
