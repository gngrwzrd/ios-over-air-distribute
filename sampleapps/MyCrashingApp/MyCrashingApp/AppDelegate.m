
#import "AppDelegate.h"

@interface AppDelegate ()
@end

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
	// Override point for customization after application launch.
	
	NSError * error;
	
	PLCrashReporter * crash = [PLCrashReporter sharedReporter];
	if([crash hasPendingCrashReport]) {
		NSLog(@"has pending crash");
		NSData * crashData = [crash loadPendingCrashReportData];
		if(crashData) {
			NSURL * url = [NSURL URLWithString:@"http://gngrwzrd.com/dist/apps/MyCrashingApp/crash/log.php"];
			NSMutableURLRequest * request = [NSMutableURLRequest requestWithURL:url];
			[request setHTTPMethod:@"POST"];
			
			PLCrashReport *report = [[PLCrashReport alloc] initWithData: crashData error: &error];
			NSString * log = [PLCrashReportTextFormatter stringValueForCrashReport:report withTextFormat:PLCrashReportTextFormatiOS];
			NSLog(@"%@",log);
			NSData * logData = [log dataUsingEncoding:NSUTF8StringEncoding];
			
			NSURLSessionUploadTask * upload = [[NSURLSession sharedSession] uploadTaskWithRequest:request fromData:logData completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
				NSLog(@"%@",error);
				NSLog(@"%@",response);
				NSLog(@"%@",data);
			}];
			
			[upload resume];
		}
	}
	
	if(![crash enableCrashReporterAndReturnError:&error]) {
		NSLog(@"Error");
	}
	
	return YES;
}

- (void)applicationWillResignActive:(UIApplication *)application {
	// Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
	// Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
}

- (void)applicationDidEnterBackground:(UIApplication *)application {
	// Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
	// If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
}

- (void)applicationWillEnterForeground:(UIApplication *)application {
	// Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
}

- (void)applicationDidBecomeActive:(UIApplication *)application {
	// Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
}

- (void)applicationWillTerminate:(UIApplication *)application {
	// Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
}

@end
