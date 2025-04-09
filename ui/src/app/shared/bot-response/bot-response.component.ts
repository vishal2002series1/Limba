import { Component, Input } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { MarkdownService } from 'ngx-markdown';
import { ContentRetrieved } from 'src/app/constants/model';

@Component({
  selector: 'app-bot-response',
  templateUrl: './bot-response.component.html',
  styleUrls: ['./bot-response.component.scss']
})
export class BotResponseComponent {
  @Input('content') content?: ContentRetrieved;
  @Input('activeTab') activeTab: string = '';

  date: string | null = null;

  constructor( private markdownService: MarkdownService, private sanitizer: DomSanitizer ){}
  
  ngOnInit(): void {
    this.formatDate();
    this.markPageContent();
  }

  //To collapse and expand collapsible box
  toggleDiv(id: string) {
    if (this.activeTab === id) {
        this.activeTab = '';
    } else {
        this.activeTab = id;
    }
  }
    
  //To turn date from dd_mm_yy to dd-mm-yy
  formatDate() {
    if (this.content) {
      if (this.content.doc_details && this.content.doc_details.publication_date) {
        this.date = this.getFormattedDate(this.content.doc_details.publication_date);
      }
    }
  }

  getFormattedDate(publicationDate: string): string {
    if (publicationDate === 'NA') {
      return 'NA';
    } else {
      const formattedDate = publicationDate.replace(/_/g, '-');
      return formattedDate;
    }
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

  markPageContent() {
    if (this.content && this.content.page_content) {
      this.content.marked_page_content = this.sanitizeMarkdown(this.content.page_content);
      this.content.sliced_page_content = this.sanitizeMarkdown(this.content.page_content.slice(0, 200));
      // console.log("Page Content: ", this.content.page_content);
      // console.log("Markdown Page Content: ", this.content.marked_page_content);
      // console.log("Sliced Page Content: ", this.content.sliced_page_content);
    }
  }
}  
