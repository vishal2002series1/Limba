import { Component, Input } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { MarkdownService } from 'ngx-markdown';
import { FinancialContent } from 'src/app/constants/model';

@Component({
  selector: 'app-financial-response',
  templateUrl: './financial-response.component.html',
  styleUrl: './financial-response.component.scss'
})
export class FinancialResponseComponent {
  @Input('financialContent') financialContent?: FinancialContent;
  @Input('activeTab') activeTab: string = '';
  
  constructor( private markdownService: MarkdownService, private sanitizer: DomSanitizer ){}
  
  ngOnInit(): void {
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
    if (this.financialContent && this.financialContent.financialString) {
      this.financialContent.markedString = this.sanitizeMarkdown(this.financialContent.financialString);
    }
  }
    
}  
