frappe.ready(function() {
    $('.new-discussion-content').textareaAutoSize();

	if(window.discussion_name) {
	    $('.new-discussion-content')
			.on("focus", function() {
				$(this).parents(".discussion-block").addClass("active");
			})
			.on("blur", function() {
				$(this).parents(".discussion-block").removeClass("active");
			})
			.on("keydown", function(e) {
		        if(e.which==13 && (e.ctrlKey || e.metaKey)) {
		            frappe.call({
		                method: "gameplan.api.add_comment",
		                args: {
		                    name: window.discussion_name,
		                    content: $('.new-discussion-content').val()
		                },
		                success: function(r) {
		                    $(r.message).appendTo('.discussion-comments');
		                    $('.new-discussion-content').val('');
		                }
		            });
		        }
		    });
	}
});
