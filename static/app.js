let sel = document.getElementById("locationOptions");
let p = document.getElementById("display");

function getSelectedOption(sel) {
	let opt;
	for (let i = 0, len = sel.options.length; i < len; i++) {
		opt = sel.options[i];
		if (opt.selected === true) {
			break;
		}
	}
	return opt;
}
// on click of Find button, show card with corresponding job

$("#showTxt").on("click", function (e) {
	e.preventDefault();
	$("#display").empty();

	let targetLocation = p.innerText;
	targetLocation = sel.options[sel.selectedIndex].text;

	let allLocations = $(".location");
	for (let obj of allLocations) {
		if (targetLocation === obj.innerText) {
			let res = obj.parentElement;
			$("#display").append(res);
			$("#display").css("border", "2px solid grey");
		}
	}
});

// strip JSON API data from html tags

$(".title").text(function () {
	return $(this)
		.text()
		.replace(/(<([^>]+)>)/gi, "");
});
$(".description").text(function () {
	return $(this)
		.text()
		.replace(/(<([^>]+)>)/gi, "");
});

// save job to favorites
$(".favorites").on("click", function (e) {
	e.preventDefault();
	$(this).css("color", "green");
	let targetdiv = $(this).closest("div");
	let obj = targetdiv[0];
	let gethtml = obj.innerHTML;
	let res = gethtml.replace("Save to Favorites", "<button class='btn btn-sm btn-danger'><i class='fas fa-trash-restore'></i></button>");
	let keyname = $(this).data("id");

	localStorage.setItem(keyname, res);
});

// get all storage data with all saved jobs
for (let i = 0; i < localStorage.length; i++) {
	// console.log(localStorage.key(i));
	$(".fav-jobs-list").append(localStorage.getItem(localStorage.key(i)) + "<hr />");
	$(".btn-danger").on("click", function () {
		window.location.reload();
		let closest = $(this).closest("a");
		let targetid = closest.attr("data-id");
		if (targetid === localStorage.key(i)) {
			localStorage.removeItem(targetid);
		}
	});
}

////////////V.2.0

// $(".events").on("click", function (e) {
// 	e.preventDefault();
// 	$(this).css("color", "green");

// 	let targetdiv = $(this).closest("a");
// 	let obj = targetdiv[0];
// 	let gethtml = obj.innerHTML;
// 	console.log(gethtml);
// 	if (gethtml.includes("<i class='far fa-star'></i>")) {
// 		$(".fa-star").remove();
// 		$(this).prepend("<i class='fas fa-star'></i>");
// 	} else {
// 		$(".fa-star").remove();
// 		$(this).prepend("<i class='far fa-star'></i>");
// 		$(this).css("color", "blue");
// 	}
// });
