import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from './shared/shared.module';
import { HttpClientModule } from '@angular/common/http';
import { ToastrModule} from 'ngx-toastr';
import { UserChatProdComponent } from './components/user-chat-prod/user-chat-prod.component';
import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { WealthChatComponent } from './components/wealth-chat/wealth-chat.component';
import { FinancialPlannerChatComponent } from './components/financial-planner-chat/financial-planner-chat.component';
import { EsgChatComponent } from './components/esg-chat/esg-chat.component';
import { TrustReviewChatComponent } from './components/trust-review-chat/trust-review-chat.component';
import en from '@angular/common/locales/en';
import { en_US, provideNzI18n } from 'ng-zorro-antd/i18n';
import { registerLocaleData } from '@angular/common';
import { UnrestrictedChatComponent } from './components/unrestricted-chat/unrestricted-chat.component';
import { HooppDemoChatComponent } from './components/hoopp-demo-chat/hoopp-demo-chat.component';
import { HomeComponent } from './components/home/home.component';
import { RetirementChatbotComponent } from './components/retirement-chatbot/retirement-chatbot.component';
import { IrahForEsgComponent } from './components/irah-for-esg/irah-for-esg.component';
registerLocaleData(en);

@NgModule({
  declarations: [
    AppComponent,
    UserChatProdComponent,
    WealthChatComponent,
    FinancialPlannerChatComponent,
    EsgChatComponent,
    TrustReviewChatComponent,
    UnrestrictedChatComponent,
    HooppDemoChatComponent,
    HomeComponent,
    RetirementChatbotComponent,
    IrahForEsgComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    SharedModule,
    TooltipModule.forRoot(),
    HttpClientModule,
    FormsModule,
    ToastrModule.forRoot({
      timeOut: 5000,
      positionClass: 'toast-bottom-center'
    })  ],
    providers: [ provideNzI18n(en_US)],
    bootstrap: [AppComponent]
})
export class AppModule { }
