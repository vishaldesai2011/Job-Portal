function handleScroll() {
    var animatedElement = document.querySelector('.nav_container');
    var scrollPosition = window.scrollY || window.pageYOffset;
  
    if (scrollPosition > 50) {
      animatedElement.classList.add('animate');
    } else {
      animatedElement.classList.remove('animate');
    }
  }

  function handleScrollAll() {
    var animatedElement = document.querySelector(".grid");
    var scrollPosition = window.scrollY || window.pageYOffset;
  
    if (scrollPosition > 200) {
      animatedElement.classList.add('animate');
    } else {
      animatedElement.classList.remove('animate');
    }
  }

  function handleScrollJob() {
    var animatedElement = document.querySelector(".grid_job");
    var scrollPosition = window.scrollY || window.pageYOffset;
  
  
    if (scrollPosition > 900) {
      animatedElement.classList.add('animate');
    } else {
      animatedElement.classList.remove('animate');
    }
  }

  // Add scroll event listener
  document.addEventListener('scroll', handleScroll);
  document.addEventListener('scroll', handleScrollAll);
  document.addEventListener('scroll', handleScrollJob);



  document.addEventListener('DOMContentLoaded', function () {
    // Trigger the animation after a short delay to ensure the image has loaded
    setTimeout(function() {
      document.querySelector('.poster').style.opacity = '1';
      document.querySelector('.top_text').style.opacity = '1';

    }, 200); // 500 milliseconds delay
  });


  function Job_call(e) {

    window.location.href="#job";
    
    /* need to stop the form sending of the form
    
     UPDATE as comment: This may not be exactly correct syntax 
     for stopping a form , look up preventing form submission */
    
    e.preventDefault();
    e.stopPropagation(); 
    
    }


    function hide(){
      var a = document.getElementById("mobile-menu");
      var b = document.getElementById("con");
      b.style.display = "none";

      var c = document.getElementById("dis_con");
      c.style.display = "none";

      var d = document.getElementById("nav_serch");
      d.style.display = "none";


      
    }

    function unhide(){
      var isMobileVersion = document.getElementsByClassName('menu-toggle is-active');
if (isMobileVersion.length > 0) {
  location.reload();
    // elements with class "snake--mobile" exist
}
else{
  
}

      
    }
    unhide();
  
  

