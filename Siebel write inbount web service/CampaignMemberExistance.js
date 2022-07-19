function CampaignMemberExistance(Inputs, Outputs) {

    // Inputs
    var MembershipNumber: chars = Inputs.GetProperty("MembershipNumber");
    var ProgramId: chars = Inputs.GetProperty("ProgramId");

    // Siebel object definitions
    var MemberBO = TheApplication().GetBusObject("LOY Member");
    var MemberBC = MemberBO.GetBusComp("LOY Member");
    var OBO = TheApplication().GetBusObject("LOY Engine Updater");
    var AttrBC = OBO.GetBusComp("LOY Member Attribute");

    // Internal variables
    var MemberExist = "";
    var Searchset = "";

    // Outputs
    var ResCode = "";
    var ResDesc = "";
    var JoinedDate = "";
    var Status = "";
    var count;
    var LastValidDate = "";
    var MemberType = "";
    var MemberId = "";
    var SubStatusValue = "";

    with (MemberBC) {
        SetViewMode(AllView);
        ActivateField("Start Date");
        ActivateField("Join Date");
        ActivateField("Id");
        ActivateField("Status");
        ActivateField("Member Type");
        ClearToQuery();

        Searchset = "[Member Number] LIKE '" + MembershipNumber + "*" + "' AND [Program Id] = '" + ProgramId;
        SetSearchExpr(Searchset);
        ExecuteQuery(ForwardOnly);
        count = Number(CountRecords());

        if (count == 0) {
            ResCode = "-905";
            ResDesc = "Number does not exists";
        } else {
            Status = GetFieldValue("Status");
            MemberType = GetFieldValue("Member Type");
            var JoinDate1 = GetFieldValue("Start Date");
            var MemberId = GetFieldValue("Id");
            var JoinDate = new Date(JoinDate1);

            // Change date to shamsi
            var Svc = TheApplication().GetService("ChangeDateToShamsi");
            var SvcInput = TheApplication().NewPropertySet();
            var SvcOutput = TheApplication().NewPropertySet();
            SvcInput.SetProperty("InputDate", JoinDate);
            Svc.InvokeMethod("ChangeDate", SvcInput, SvcOutput);
            var DateShamsi = SvcOutput.GetProperty("OutputDate");
            DateShamsi = DateShamsi.split(' ')[0];
            JoinedDate = DateShamsi;
            if (Status == "Active") {
                if (MemberType == "Household"){
                    with (AttrBC) {
                        SetViewMode(AllView);
                        ClearToQuery();
                        ActivateField("Value");
                        ActivateField("Attribute Name");
                        ActivateField("Attribute Definition Id");
                        Searchset =
                          "[Member Id] = '" +
                          MemberId +
                          "' AND [Program Id] = '" +
                          ProgramId +
                          "' AND [Attribute Name] = 'Member sub-status'";
                        SetSearchExpr(Searchset);
                        ExecuteQuery(ForwardOnly);
                
                        if (CountRecords() > 0) {
                          SubStatusValue = GetFieldValue("Value");
                        }
                      }
                      if (SubStatusValue == "Active"){
                        ResCode = "0";
                        ResDesc = "The number exists in Campaign and Renew offer is Enabled";
                      } else if (SubStatusValue == "" || SubStatusValue == "Suspended"){
                        ResCode = "-920";
                        ResDesc = "The number exists in Campaign but Renew offer is Disabled";
                      }
                } else {
                    ResCode = "0";
                    ResDesc = "The number exists in Campaign and Renew offer is Enabled";
                }
            } else if (Status == "Cancelled") {
                ResCode = "-901";
                ResDesc = "The subscriber used to be in Member but currently it does not exist in Campaign";
            }
        }
    }

    Outputs.SetProperty("ResponseCode", ResCode);
    Outputs.SetProperty("ResponseDescription", ResDesc);
    Outputs.SetProperty("JoinedDate", JoinedDate);
    Outputs.SetProperty("LastValidDate", LastValidDate);
    Outputs.SetProperty("Status", Status);
    Outputs.SetProperty("MemberType", MemberType);

    MemberBO = "";
    MemberBC = "";
}