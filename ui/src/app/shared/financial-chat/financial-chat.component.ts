import { Component, ElementRef, Input, OnInit, SimpleChanges, ViewChild, ViewEncapsulation } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup } from '@angular/forms';
import { take } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { TabsetComponent } from 'ngx-bootstrap/tabs';
import { ChatResponse, Client, ContentResponse, ContentRetrieved } from 'src/app/constants/model';
import { UserChatService } from 'src/app/shared/services/user-chat.service';
import { MarkdownService } from 'ngx-markdown';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-financial-chat',
  templateUrl: './financial-chat.component.html',
  styleUrls: ['./financial-chat.component.scss'],
  encapsulation: ViewEncapsulation.None 
})
export class FinancialChatComponent implements OnInit {

  @Input('client') client!: Client;
  web_page_type: string = 'irah/chat/financial_planner';
  loader = false;
  // params!: Params;
  chatForm!: FormGroup;
  messages: ChatResponse[] = [];
  activeTab: string = '';
  chunkSize: number = 500;
  currentIndex: number = 0;
  @ViewChild('scrollme', { static: true }) private scollContainer?: ElementRef<HTMLDivElement>;
  toogleSidebar = false;
  @ViewChild('tabset') tabset: TabsetComponent | undefined;
  query_type: string | undefined;
  isQueryConditionTrue: boolean = false;
  contentUsed: ContentRetrieved[] = [];
  content: ContentRetrieved[] = [];
  disableForm: boolean = false;
  customEditIconStr = 'Custom edit icon and tooltip text.';
  tips = ['Retrieving the answer...', 'Almost there...', 'Just a moment...'];
  currentTipIndex = 0;
  currentTip = this.tips[this.currentTipIndex];


  constructor(private userChat: UserChatService,
    private router: Router, private route: ActivatedRoute,
    private toastr: ToastrService,
    private userChatService: UserChatService,
    private markdownService: MarkdownService, 
    private sanitizer: DomSanitizer) {
      this.startTipRotation();
  }

  // Query Search Form
  queryForm() {
    this.chatForm = new FormGroup({
      query: new FormControl('')
    });
  }

  get query() {
    return this.chatForm.get('query')!;
  }

  // Submit user query
  submitQuery(): void {
    if (this.disableForm) return;

    let askedQuestion = this.query.value;
    
    if (askedQuestion === '') return;

    this.messages.push({ type: 'user', query: this.chatForm.value.query });
    setTimeout(() => {
      if (this.scollContainer?.nativeElement) {
        this.scollContainer.nativeElement.scrollTop = this.scollContainer.nativeElement.scrollHeight + 750;
      }
    }, 100);

    this.queryForm();
    this.loader = true;
    const client_name = this.client.client_data.name
      this.userChat.getQueryResultFinancial(
        askedQuestion, this.web_page_type, client_name, this.client
      ).pipe(take(1),
      catchError((error) => {
        this.toastr.error('Error occurred while processing your request');
        const botResponse = error && error.error ? error.error : { message: 'Unknown error occurred' };
        botResponse.response = "Error occurred while processing your request";
        return of(botResponse);
      })).subscribe((botResponse: ContentResponse) => {

        // console.log(botResponse);

        this.query_type = botResponse.query_type;
        const validateQueryType = ['Client Data related Question', 'Negative Case Question'];
        if (botResponse?.query_type) this.isQueryConditionTrue = validateQueryType.includes(botResponse?.query_type);
              
        if (!this.isQueryConditionTrue) {

          if (botResponse.annotations) {
            if (!botResponse.financialContent) {
              botResponse.financialContent = [];
            }

            if (botResponse.annotations.solution_plan) {
              botResponse.financialContent.push({
                financialType: 'Solution Plan',
                financialString: botResponse.annotations.solution_plan
              });
            }
          
            if (botResponse.annotations.reasoning_steps) {
              botResponse.financialContent.push({
                financialType: 'Reasoning Steps',
                financialString: botResponse.annotations.reasoning_steps
              });
            }

          }

            if (botResponse.annotations && botResponse.annotations.ContentSearchTool){
            //   for (let i = 0; i < botResponse.annotations.ContentSearchTool.content_retrieved.length; i++) {
            //     // Set showMore to false for each subarray element
            //     botResponse.annotations.ContentSearchTool.content_retrieved[i].showMore = false;
                
            //     this.fetchDocumentLinkAndUpdateUrl(botResponse.annotations.ContentSearchTool.content_retrieved[i]);

            //     const retrievedId = botResponse.annotations.ContentSearchTool.content_retrieved[i].content_id.trim();
            //     const usedId = botResponse.annotations.ContentSearchTool.content_used[0].trim();
                
            //     if (retrievedId == usedId) {
            //       this.contentUsed.push(botResponse.annotations.ContentSearchTool.content_retrieved[i]); 
            //     } else {
            //       this.content.push(botResponse.annotations.ContentSearchTool.content_retrieved[i]);
            //     }
            //   }
                        
              for (let i = 0; i < botResponse.annotations.ContentSearchTool.content_used.length; i++) {
                // Set showMore to false for each subarray element
                botResponse.annotations.ContentSearchTool.content_used[i].showMore = false;
                
                this.fetchDocumentLinkAndUpdateUrl(botResponse.annotations.ContentSearchTool.content_used[i]);
                this.contentUsed.push(botResponse.annotations.ContentSearchTool.content_used[i]); 
              }
            
              for (let i = 0; i < botResponse.annotations.ContentSearchTool.other_relevant_content.length; i++) {
                // Set showMore to false for each subarray element
                botResponse.annotations.ContentSearchTool.other_relevant_content[i].showMore = false;
                
                this.fetchDocumentLinkAndUpdateUrl(botResponse.annotations.ContentSearchTool.other_relevant_content[i]);
                this.content.push(botResponse.annotations.ContentSearchTool.other_relevant_content[i]);
              }

            }

            botResponse.marked_response = this.sanitizeMarkdown(botResponse.response);
            botResponse.copy_response = this.convertMarkdownToCopyableText(botResponse.response);
            // console.log(botResponse.response);

          }

          this.messages.push({
            type: 'bot',
            response: botResponse,
          })

          this.toogleSidebar = true;
          this.loader = false;
        }, err => {
          if (err?.status === 500) {
            this.loader = false;
            this.toastr.error(err.statusText);
          }
        }
      )
    // }
  }

  // Scroll to top
  scrollTop() {
    setTimeout(() => {
      if (this.scollContainer?.nativeElement) {
        this.scollContainer.nativeElement.scrollTop = this.scollContainer.nativeElement.scrollHeight + 750;
      }
    }, 100)
  }

  ngOnInit(): void {
    this.queryForm();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['client'] && changes['client'].currentValue) {
      this.submitQuery();
    }
  }

  fetchDocumentLinkAndUpdateUrl(contentItem: ContentRetrieved): void {
    const path = contentItem.doc_path; 
    const filename = contentItem.doc_name;

    this.userChatService.getDocumentLink(path, filename)
      .subscribe(response => {
        contentItem.made_url = response;
      });
  }  
  
    //Markdown Formatting
    sanitizeMarkdown(markdown: string): SafeHtml | Promise<SafeHtml> {
      const parsed = this.markdownService.parse(markdown);
      if (parsed instanceof Promise) {
        return parsed.then(html => this.sanitizer.bypassSecurityTrustHtml(html));
      } else {
        return this.sanitizer.bypassSecurityTrustHtml(parsed);
      }
    }
  
    convertMarkdownToCopyableText(markdownStr: string): string {
      // Split the markdown string into lines
      const lines = markdownStr.split('\n');
      
      // Process each line
      const processedLines = lines.map(line => {
        // Remove bold formatting
        let processedLine = line.replace(/\*\*/g, '');
        // Remove heading formatting
        processedLine = processedLine.replace(/\#\#\#/g, '');
        // Convert lines starting with '-' to bullet points
        if (processedLine.trim().startsWith('-')) {
          processedLine = '• ' + processedLine.trim().substring(1).trim();
        }
        
        return processedLine;
      });
      
      // Join the processed lines back into a single string
      return processedLines.join('\n');
    }
  
    startTipRotation() {
      setInterval(() => {
        this.currentTipIndex = (this.currentTipIndex + 1) % this.tips.length;
        this.currentTip = this.tips[this.currentTipIndex];
      }, 3000);
    }
}
