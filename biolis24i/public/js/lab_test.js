frappe.ui.form.on('Lab Test', {
  refresh: function(frm) {
      frm.add_custom_button(__('Sync Biolis-24i'), function() {
          // Get the selected patient's patient_id
    var patient_id = cur_frm.doc.patient_id
    if(!patient_id){
      frappe.show_alert("Patient Id Not Found for Patient: "+ cur_frm.doc.patient, 5);
      return;
    }
    console.log("Selected Patient id is ::: ", cur_frm.doc.patient_id)
    // Pass the selected patient's patient_id to the override method
    frappe.call({
      method: "biolis24i.override.SyncTestResults",
      args: {patient_id: patient_id},
      callback: function(r) {
          console.log("sql server response :: ", r.message)
        // Loop through the list of dictionaries in the response
        frappe.model.set_value(d.doctype, d.name, "sample_id", r.message.SAMP_ID);
        $.each(cur_frm.doc.normal_test_items, function(i, d) {
          // Set the result to 0 by default
          frappe.model.set_value(d.doctype, d.name, "result_value", "N/A");
          
          // Loop through the list of dictionaries in the response
          for (var i = 0; i < r.message.length; i++) {
            if (d.lab_test_name === r.message[i].ITEM_NAME) {
              // Update the result if the test name matches
              if (r.message[i].RESULTS === 0) {
                r.message[i].RESULTS = "N/A";
              }
              console.log("Test name : ",d.lab_test_name," result updated : ",r.message[i].RESULTS)
              frappe.model.set_value(d.doctype, d.name, "result_value", r.message[i].RESULTS);
              break;
            }
          }
        });
        frappe.show_alert("Test Results Synced for Patient "+ cur_frm.doc.patient, 5);
        frm.refresh_field("normal_test_items");
      }
    });
  });
}
});

