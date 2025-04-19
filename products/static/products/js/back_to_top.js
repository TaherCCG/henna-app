$(document).ready(function() {            
    // Scroll to top when .btt-link is clicked
    $(document).on('click', '.btt-link', function(e) {
        e.preventDefault(); 
        console.log('btt-link clicked');
        window.scrollTo(0, 0);
    });

    // Handle sorting change
    $('#sort-selector').change(function() {
        let selector = $(this);
        let currentUrl = new URL(window.location);
        let selectedVal = selector.val();

        // Update the selected option visually
        selector.find('option').each(function() {
            if (this.value === selectedVal) {
                $(this).prop('selected', true);
            } else {
                $(this).prop('selected', false);
            }
        });
    
        if (selectedVal !== "reset") {
            let [sort, direction] = selectedVal.split("_");
            currentUrl.searchParams.set("sort", sort);
            currentUrl.searchParams.set("direction", direction);
            window.location.replace(currentUrl);
        } else {
            currentUrl.searchParams.delete("sort");
            currentUrl.searchParams.delete("direction");
            window.location.replace(currentUrl);
        }
    });
});
