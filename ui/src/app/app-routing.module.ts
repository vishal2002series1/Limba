import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserChatProdComponent } from './components/user-chat-prod/user-chat-prod.component';
import { WealthChatComponent } from './components/wealth-chat/wealth-chat.component';
import { FinancialPlannerChatComponent } from './components/financial-planner-chat/financial-planner-chat.component';
import { EsgChatComponent } from './components/esg-chat/esg-chat.component';
import { TrustReviewChatComponent } from './components/trust-review-chat/trust-review-chat.component';
import { UnrestrictedChatComponent } from './components/unrestricted-chat/unrestricted-chat.component';
import { HooppDemoChatComponent } from './components/hoopp-demo-chat/hoopp-demo-chat.component';
import { RetirementServicePortalComponent } from './components/retirement-service-portal/retirement-service-portal.component';
import { HomeComponent } from './components/home/home.component';
import { RetirementChatbotComponent } from './components/retirement-chatbot/retirement-chatbot.component';
import { IrahForEsgComponent } from './components/irah-for-esg/irah-for-esg.component';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent, title: 'IRAH - Home' },
  { path: 'chat', component: UserChatProdComponent, title: 'IRAH - Custom Chat' },
  { path: 'chat/wealth', component: WealthChatComponent, title: 'IRAH - Wealth Chat' },
  { path: 'chat/financial-planner', component: FinancialPlannerChatComponent, title: 'IRAH - Financial Planner Chat' },
  { path: 'chat/esg-demo', component: EsgChatComponent, title: 'IRAH - ESG Chat' },
  { path: 'chat/irah-for-esg', component: IrahForEsgComponent, title: 'IRAH For ESG' },
  { path: 'chat/trust_review', component: TrustReviewChatComponent, title: 'IRAH - Trust Review Chat' },
  { path: 'chat/unrestricted', component: UnrestrictedChatComponent, title: 'IRAH - Unrestricted Chat' },
  { path: 'chat/pe-pension-demo', component: HooppDemoChatComponent, title: 'IRAH - Private Equity Pension Demo Chat' },
  { path: 'chat/retirement-service-portal', component: RetirementServicePortalComponent, title: 'IRAH - Retirement Service Portal' },
  { path: 'chat/retirement-chatbot', component: RetirementChatbotComponent, title: 'IRAH - Retirement Chatbot' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
