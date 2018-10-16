/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
// binary search
bool search(int needle, int haystack[], int n)
{
    // false if n is non-positive
    if (n < 0)
    {
        return false;
    }
    
    // define start, middle, & end
    int start = 0;
    int end = n - 1;
    int mid = (start + end) / 2;


    while (start <= end)
    {
        // if needle is in the middle, return true, else keep dividing haystack
        if (haystack[mid] == needle)
        {
            return true;
        }
        else if (haystack[mid] < needle)
        {
            start = mid + 1;
        }
        else
        {
            end = mid - 1;
        }
        // redefine middle
        mid = (start + end) / 2;
    }
    return false;
}

/**
 * Sorts array of n values.
 */
// bubble sort
void sort(int haystack[], int n)
{
    
    // define bool switch iterate, substitute m for n
    bool iterate;
    int m = n;

    do
    {
        // if no (more) values to sort, end loop
        iterate = false;
        
        // shorten sortable list by 1 at the end with every loop
        m -= 1;
        
        // iterate over list
        for (int i = 0; i < m; i++)
        {
            // compare adjacent elements
            if (haystack[i] > haystack[i + 1])
            {
                // swap elements if in wrong order
                int temp = haystack[i];
                haystack[i] = haystack[i + 1];
                haystack[i + 1] = temp;
                iterate = true;
            }
        }
    }
    while (iterate);

    return;
}

/*
//counting sort
void sort(int haystack[], int n)
{
    // let's create an array the the size of max number that can be generated
    char x[65536] = {0};
    
    // for every generated number we add 1 (kinda like ticks) to corresponding address in array
    for (int o = 0; o < n; o++)
    {
        x[haystack[o]]++;
    }
    
    int z = 0;
    
    // for every tick we put the address of the tick in original array aka haystack
    for (int p = 0; p < 65536; p++)
    {
        // yay, it works!
        for ( ; x[p] > 0; x[p]--)
        {
        haystack[z] = p;
        //printf("haystack[%i] is %i\n", z, haystack[z]);
        z++;
        }
    }
}
*/


//merge sort
void sort(int haystack[], int n)
{
    merge_sort(haystack, 0, n - 1)
}

void merge_sort(int haystack[], int left, int right)
{
    if (right > left)
    {
        int mid = n / 2;
        merge_sort(haystack[], left, mid); 
        merge_sort(haystack[], mid + 1, right);
        merge();
    }
}
    
    
    
    
    
    int mid = n / 2;
    char left[];
    char right[];
    
    if (n <= 1) 
    {
        
    } 
    else 
    {
        for (int i = 0; i < mid; i++) {
            left[i] = haystack[i];
            
            
            right[i] = haystack[mid + i];
              
        
    
    
    
    
    
    
    
    