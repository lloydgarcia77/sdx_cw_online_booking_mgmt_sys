$(document).ready(function(){   
    //Get the button
    let mybutton = $("#back-to-top");

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function() {scrollFunction()};

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            // mybutton.style.display = "block";
            mybutton.fadeIn();
        } else {
            // mybutton.style.display = "none";
            mybutton.fadeOut();
        }
    }

    // When the user clicks on the button, scroll to the top of the document
    function topFunction() {
        // document.body.scrollTop = 0;
        // document.documentElement.scrollTop = 0;
        window.scrollTo({top: 0, behavior: 'smooth'});
    }

    mybutton.on("click", topFunction);
 
});