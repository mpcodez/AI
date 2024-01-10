/*******************************************************
* 
* Medha Pappula
* Thomas Jefferson High School for Science and Technology
* Junior-5 Division
* Contest #2 2022-2023
* Binary Counting
* 
********************************************************/

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class binaryCounting_Medha_Pappula{

   public static void main(String[] args) throws FileNotFoundException{
   
      Scanner scan = new Scanner(new File("2jr_testdata.txt"));
      while(scan.hasNext()){
      
         System.out.println(count(scan.nextLine()));
         
      }

   }
   
   public static int count(String line){
   
      String[] letters = line.split("");
      String binary = "";
         
      for(int i = 0; i < letters.length; i++){
         int ascii = (int)letters[i].charAt(0);
         String num = Integer.toString(ascii, 2);
         num = "0".repeat(8-num.length()) + num;
         binary += num;
      }
      
      int count = 0, index = binary.indexOf(Integer.toString(0, 2)), highIndex = 0;
      String highNum = "";
      
      while(index != -1){
         highNum = Integer.toString(count,2);
         count = count + 1;
         index = binary.indexOf(Integer.toString(count, 2));
      }
      
      return Integer.parseInt(highNum, 2);
   }
   
   
}