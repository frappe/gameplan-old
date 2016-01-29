frappe.ready(function() {
	frappe.socket.init();
	$('.new-discussion-content').textareaAutoSize();
});

var gameplan = {
	setup_dropfile: function() {
		$(document).on('dragenter dragover', false)
			.on('drop', function (e) {
				var dataTransfer = e.originalEvent.dataTransfer;
				if (!(dataTransfer && dataTransfer.files
					&& dataTransfer.files.length > 0)) {
					return;
				}
				e.stopPropagation();
				e.preventDefault();

				$.each(dataTransfer.files, function(i, fileobj) {
					// render files
					var freader = new FileReader();
					freader.onload = function() {
						var dataurl = freader.result;
						var $img = $('<div data-name="'
							+ fileobj.name +'" class="discussion-thumb" \
							style="background-image:url('+ dataurl +');">\
							<span class="pull-right close">&times;</span>\
							</div>')
							.appendTo('.discussion-thumb-list.is-editable');

						$img.find('.close').on('click', function() {
							$img.remove();
						});

					};
					freader.readAsDataURL(fileobj);
				});
			});
	},
	get_files: function() {
		var files = [];
		$('.discussion-thumb-list.is-editable .discussion-thumb').each(
			function() {
				files.push({
					name: $(this).attr('data-name'),
					content: $(this).css('background-image').slice(5, -2)
				});
			});

		return files;
	}

}
