// Basic interactivity for logo, search and login dropdown
document.addEventListener('DOMContentLoaded', function(){
	const logo = document.getElementById('logo');
	const searchForm = document.getElementById('searchForm');
	const searchInput = document.getElementById('searchInput');
	const loginBtn = document.getElementById('loginBtn');
	const loginMenu = document.getElementById('loginMenu');
	const dropdownLi = loginBtn && loginBtn.parentElement;

	if(logo){
		logo.addEventListener('click', ()=>{
			logo.classList.add('pulse');
			setTimeout(()=> logo.classList.remove('pulse'), 500);
			window.scrollTo({ top:0, behavior:'smooth'});
		});
	}

	if(searchForm){
		searchForm.addEventListener('submit', function(e){
			e.preventDefault();
			const q = searchInput.value.trim();
			if(!q) {
				searchInput.focus();
				return;
			}
			// For now, just log search and highlight result area
			console.log('Search query:', q);
			alert('Search for: ' + q + '\n(No backend yet - frontend prototype)');
		});
	}

	if(loginBtn && loginMenu && dropdownLi){
		loginBtn.addEventListener('click', function(e){
			e.stopPropagation();
			const open = dropdownLi.classList.toggle('open');
			loginMenu.setAttribute('aria-hidden', String(!open));
		});

		// close when clicking outside
		document.addEventListener('click', function(){
			dropdownLi.classList.remove('open');
			loginMenu.setAttribute('aria-hidden','true');
		});
	}
	// smooth in-page scrolling for anchor links
	document.querySelectorAll('a[href^="#"]').forEach(function(a){
		a.addEventListener('click', function(e){
			const href = a.getAttribute('href');
			if(href.length>1){
				const target = document.querySelector(href);
				if(target){
					e.preventDefault();
					target.scrollIntoView({ behavior: 'smooth', block: 'start' });
				}
			}
		});
	});

	// About editor (frontend-only, persists to localStorage)
	(function(){
		const aboutImage = document.getElementById('aboutImage');
		const aboutImageInput = document.getElementById('aboutImageInput');
		const chooseImageBtn = document.getElementById('chooseImageBtn');
		const editBtn = document.getElementById('editAboutBtn');
		const aboutView = document.getElementById('aboutView');
		const aboutDesc = document.getElementById('aboutDesc');
		const aboutEditForm = document.getElementById('aboutEditForm');
		const aboutDescInput = document.getElementById('aboutDescInput');
		const saveBtn = document.getElementById('saveAboutBtn');
		const cancelBtn = document.getElementById('cancelAboutBtn');

		if(!aboutImage) return;

		// load saved data
		const savedDesc = localStorage.getItem('about_description');
		const savedImage = localStorage.getItem('about_image');
		if(savedDesc) aboutDesc.textContent = savedDesc;
		if(savedImage) aboutImage.src = savedImage;

		let currentImageData = savedImage || aboutImage.src;

		editBtn.addEventListener('click', function(){
			aboutEditForm.style.display = '';
			aboutView.style.display = 'none';
			aboutDescInput.value = aboutDesc.textContent.trim();
		});

		chooseImageBtn.addEventListener('click', function(){
			aboutImageInput.click();
		});

		aboutImageInput.addEventListener('change', function(e){
			const file = e.target.files && e.target.files[0];
			if(!file) return;
			const reader = new FileReader();
			reader.onload = function(ev){
				aboutImage.src = ev.target.result;
				currentImageData = ev.target.result; // data URL
			};
			reader.readAsDataURL(file);
		});

		saveBtn.addEventListener('click', function(e){
			e.preventDefault();
			const newDesc = aboutDescInput.value.trim();
			aboutDesc.textContent = newDesc || 'No description provided.';
			// persist
			localStorage.setItem('about_description', aboutDesc.textContent);
			if(currentImageData) localStorage.setItem('about_image', currentImageData);
			aboutEditForm.style.display = 'none';
			aboutView.style.display = '';
		});

		cancelBtn.addEventListener('click', function(){
			// revert preview to saved
			const saved = localStorage.getItem('about_image');
			aboutImage.src = saved || currentImageData;
			aboutEditForm.style.display = 'none';
			aboutView.style.display = '';
		});

	})();
});

