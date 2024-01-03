import java.util.*;
import java.io.*;
 
public class Main {
  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
 
    int n = Integer.parseInt(br.readLine());
    String str = br.readLine();
    
    int ans = 0;
    int startInfected = 0;
    
    // check if atleast one cow is infected and save the final state
    boolean cowInfected = false;
    String finalState = "";
    
    for(int i=0; i<n; i++) {
      char c = str.charAt(i);
      if(c == '1') {
        cowInfected = true;
      }
      finalState += c;
    }
    
    // check for all possible initial states and number of nights
    for(int i=0; i<n; i++) {
      String newState = ""; 
      
      // Assume that ith cow was the first infected cow
      for(int j=0; j<=i; j++) {
        newState += '1'; // cow infected by the ith cow
      }
      
      for(int j=i+1; j<n; j++) {
        newState += '0'; // cow not infected by the ith cow
      }
      
      // simulate the nights spreading the sickness
      boolean isPossible = true;
      for(int j=0; j<n; j++) {
        if(newState.equals(finalState)) {
          break;
        }
        
        if(newState.charAt(j) == '1') {
          if(j != 0) {
            newState = newState.substring(0, j-1) + '1' + newState.substring(j-1 + 1);
          }
          
          if(j != n-1) {
            newState = newState.substring(0, j+1+1) + '1' + newState.substring(j+1+1 + 1);
          }
        }
      }
      
      // check if the final state is possible
      if(newState.equals(finalState)) {
        if(cowInfected) {
          ans++;
        } else {
          startInfected++;
        }
      }
    }
 
    if(cowInfected) {
      System.out.println(ans);
    } else {
      System.out.println(startInfected);
    }
  }
}